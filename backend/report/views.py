import copy
from report.utils.bugs_statistics import stats,test_summary

from report.utils.feature_wise_summary import feature_wise_summary
from report.utils.fetch_severity import fetch_severity
from report.utils.test_progress import test_progress
from users.authorize import user_authorization
import json
import logging
import pandas as pd
from dotenv import load_dotenv

from django.db import transaction
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from project.utils import CustomException
from report.data_processing_function import data_processing

from project.models import Projects
from project.views import user_details, has_access_to_project
from project import project_error

from report.excel_utils import read_excel_file
from report.models.test_cases import SweepBugs, TestCases, Sweep
from report.models.testcase_result import TestcaseResult
from report.serializer import TestCaseSerializer
from report.models.summary import Summary
from report import report_errors
from report import report_error
from report.testcase_validation import testcase_validation
from report.utils.report_export_to_excel import export_to_excel
from report.utils.util import feature_wise_bug_count, project_exists, check_project_exists

logger = logging.getLogger(__name__)
import re

load_dotenv()

COVER_AND_VERSION = "Cover & Version"
AMENDMENT_TC = "Amendment of TC"
UNNAMED_ONE = "Unnamed: 1"
INTERNAL_SERVER_ERROR = Response({"message ": "internal server error "}, status=500)

def generate_dynamic_column_mapping(columns):
    dynamic_mapping = {}
    static_columns = {
        UNNAMED_ONE: "Sl. No.",
        "Unnamed: 2": "test_case_id",
        "Unnamed: 3": "description",
        "Unnamed: 4": "feature",
        "Unnamed: 5": "sub_feature",
        "Unnamed: 6": "test_steps",
        "Unnamed: 7": "pre_condition",
        "Unnamed: 8": "expected_results",
        "Unnamed: 9": "category",
    }

    header_pattern = re.compile(r"^(Actual Result|Build|Pass/ Fail|Bug ID|Comments)(\.(\d+))?$")
    dynamic_column_count = {}
    status_column_indices = [i for i, col in enumerate(columns) if re.match(r"Unnamed:\s*1\d", col, re.IGNORECASE)]

    for i, column in enumerate(columns):
        match = header_pattern.match(column)
        if match:
            header, _, index = match.groups()
            if index is None:
                dynamic_column_name = header
            else:
                dynamic_column_name = f"{header}.{index}"
            if header not in dynamic_column_count:
                dynamic_column_count[header] = 0
            dynamic_mapping[column] = f"{dynamic_column_name}.{dynamic_column_count[header]}"
            dynamic_column_count[header] += 1
        elif column in static_columns:
            dynamic_mapping[column] = static_columns[column]
        elif i in status_column_indices:
            dynamic_mapping[column] = "status"
        elif re.match(r"Unnamed:\s*(2[3-9]|[3-4]\d|50)", column, re.IGNORECASE):
            dynamic_mapping[column] = "comments"
    return dynamic_mapping


def get_column_value(row_data, dynamic_column_mapping, key, index=0):
    variations = [f"{key}.{index}", key]

    for variation in variations:

        if variation in dynamic_column_mapping:
            return row_data.get(dynamic_column_mapping[variation], "")
    return ""


def sweep_validation(bug_ids, row_number, sheet_name, error_dict=None):
    if error_dict is None:
        error_dict = {}    
    if bug_ids and bug_ids[0].strip().lower() == "fail":
        has_bug_id = False
        for bug_id in bug_ids[1:]:
            if bug_id != "":
                has_bug_id = True
                break

        if not has_bug_id:
            field_name = "bug_ids"
            error_code = 1111
            error_dict.setdefault("errors", {})[field_name] = {
                "error_code": error_code,
                "message": f"[Sheet: {sheet_name}, Row: {row_number}] No valid bug ID found in the same row when the status is 'Fail'."
            }
    return error_dict


def map_status(row_data):
    status_column_key = None
    for key in row_data.keys():
        if "status" in key.lower():
            status_column_key = key
            break
    return status_column_key

def bug_id_dynamic_fetch(dynamic_column_mapping,row_data,bug_ids_row):
    for column_name in dynamic_column_mapping:
        if column_name.startswith("Bug ID"):
            bug_id = get_column_value(row_data, dynamic_column_mapping, column_name)
            bug_ids_row.append(bug_id)
    return bug_ids_row  

def get_sheet_row_number(row_sheet, sheet_name):
    if sheet_name not in row_sheet:
        row_sheet[sheet_name] = 1
    return row_sheet[sheet_name]


def process_test_cases(dynamic_sheets_data, project_id, dynamic_column_mapping):
    errors = []
    test_cases = []
    row_datas = []
    row_sheet={}

    for row_number,row_data in enumerate(dynamic_sheets_data, start=1):
        sheet_name = row_data.get("sheet_name", "")

        if (
                UNNAMED_ONE in dynamic_column_mapping
                and row_data.get(dynamic_column_mapping.get(UNNAMED_ONE, "")) != "Sl. No."
        ):
            sheet_row_number = get_sheet_row_number(row_sheet,sheet_name)

            error_dict = {}
            test_case_id = row_data.get(
                dynamic_column_mapping.get("Unnamed: 2", ""), ""
            )
            feature = row_data.get(dynamic_column_mapping.get("Unnamed: 4", ""), "")
            status_column_key=map_status(row_data)  
            status = str(row_data.get(status_column_key, None))
            
            error_dict_copy = copy.deepcopy(error_dict)
            error_dict_copy = testcase_validation(
                test_case_id,
                feature,
                status,
                sheet_row_number,
                sheet_name,
                error_dict_copy,
            )
            bug_ids_row = [status]
            bug_ids_row=bug_id_dynamic_fetch(dynamic_column_mapping,row_data,bug_ids_row)
            sweep_error_dict = copy.deepcopy(error_dict_copy)

            sweep_error_dict = sweep_validation(
                bug_ids_row,
                sheet_row_number,
                sheet_name,
                sweep_error_dict,
            )

            if sweep_error_dict:
                errors.append(sweep_error_dict)

            if error_dict:
                errors.append(error_dict)
            if not error_dict and not sweep_error_dict:
                test_case = TestCases.objects.filter(
                    test_case_id=test_case_id,
                    sheet_name=sheet_name,
                    project_id=project_id,
                ).first()
                test_cases.append(test_case)
                row_datas.append(row_data)
            row_sheet[sheet_name] += 1

    return errors, test_cases, row_datas


def check_sheet_for_process(sheet_df, sheet_name, dynamic_sheets_data):
    dynamic_column_mapping = {}
    dynamic_column_mapping = generate_dynamic_column_mapping(
        sheet_df.columns.tolist()
    )
    sheet_df.rename(columns=dynamic_column_mapping, inplace=True)
    for row in sheet_df.to_dict(orient="records"):
        row["sheet_name"] = sheet_name
        dynamic_sheets_data.append(row)
    return dynamic_sheets_data, dynamic_column_mapping


@api_view(["POST"])
@user_authorization
def import_data_from_summary(request, project_id, sweep_count, ui_or_api):
    try:
        project_id = int(project_id)
        sweep_count = int(sweep_count)
        if sweep_count > 4:
            return Response(
            report_errors.INVALID_VALUE, status=status.HTTP_404_NOT_FOUND
            )
        Projects.objects.get(id=project_id)
    except Projects.DoesNotExist:
        return Response(
            project_error.PROJECT_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
        )

    except ValueError:
        return Response(
            report_errors.INVALID_VALUE, status=status.HTTP_404_NOT_FOUND
        )
    try:
        if not request.FILES["file"].name.endswith(".xls") and not request.FILES[
            "file"
        ].name.endswith(".xlsx"):
            return Response(
                report_errors.INVALID_FORMAT, status=status.HTTP_400_BAD_REQUEST
            )
        if ui_or_api not in ["UI", "API"]:
            return Response(report_errors.UI_OR_API, status=status.HTTP_404_NOT_FOUND)
        file_path = request.FILES["file"]
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.expand_frame_repr", False)

        excel_sheet_names = pd.ExcelFile(file_path).sheet_names
        sheet_configs = {
        }
        cover_and_version_data = []
        amendment_of_tc_data = []
        summary_data = []
        dynamic_sheets_data = []
        all_errors = []
                        
        dynamic_sheet_names = excel_sheet_names[3:]
        for dynamic_sheet_name in dynamic_sheet_names:
            sheet_configs[dynamic_sheet_name] = {
                "skiprows": 6,
                "header_rows": 0,
            }
            skiprows = sheet_configs[dynamic_sheet_name]["skiprows"]
            header_rows = sheet_configs[dynamic_sheet_name]["header_rows"]
            sheet_df = read_excel_file(file_path, dynamic_sheet_name, skiprows, header_rows)
            dynamic_sheets_data, dynamic_column_mapping = check_sheet_for_process(
                sheet_df, dynamic_sheet_name, dynamic_sheets_data
            )
            
            if sheet_df.empty:
                return Response(
                    report_errors.EMPTY_FILE, status=status.HTTP_400_BAD_REQUEST
                )

        with transaction.atomic():
            try:
                errors, test_case, row_data = process_test_cases(
                    dynamic_sheets_data, project_id, dynamic_column_mapping
                )
                if errors:
                    all_errors.extend(errors)

            except IntegrityError:
                return Response(
                    report_errors.DATA_INTEGRITY_ERROR,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            except Exception:
                return Response(
                    report_errors.DATA_PROCESS_ERROR,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if all_errors:
            return Response(all_errors, status=400)

        else:
            data_processing(
                sheet_configs,
                file_path,
                cover_and_version_data,
                amendment_of_tc_data,
                summary_data,
                test_case,
                row_data,
                project_id,
                dynamic_column_mapping,
                sweep_count,
                ui_or_api
            )
            return Response(
                report_errors.DATA_PROCESS_SUCCESS, status=status.HTTP_200_OK
            )

    except Exception:
        return Response(
            report_errors.DATA_PROCESS_ERROR,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@user_authorization
def list_all_page_name(request):
    try:
        api_or_ui = request.GET.get("testCaseCategory")
        project_id = int(request.GET.get("projectid"))
        try:
            user = user_details(request)
            user_access = has_access_to_project(user.id, project_id)
            if not user_access:
                return Response(
                    project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
                )
            Projects.objects.get(pk=project_id)
        except Exception:
            return Response(
                project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
            )

       
        sheet_names_db = list(TestCases.objects.filter(
            project_id=project_id, test_case_choice=api_or_ui).values_list('sheet_name', flat=True).distinct())
        combined_sheet_names =  sheet_names_db
        if len(sheet_names_db) == 0:
            return Response(
                report_error.EXCEL_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"sheet_names": combined_sheet_names})
    except Exception:
        return Response({"error": "An error occurred"}, status=500)

def get_bug_ids_for_sweep(sweep_id):
    try:
        sweep = Sweep.objects.get(id=sweep_id)
        bug_ids = list(SweepBugs.objects.filter(sweep=sweep).values_list('bug_id', flat=True))
        return bug_ids
    except Sweep.DoesNotExist:
        return None  


@api_view(["GET"])
@user_authorization
def list_sheet_details(request):
    try:
        list_and_update_sheet_validation(request)
        project_id = request.GET.get("projectid")
        sheet_name = request.GET.get("sheetname")
        api_or_ui = request.GET.get("testCaseCategory")
        test_cases = TestCases.objects.filter(
            project_id=project_id, sheet_name=sheet_name,test_case_choice=api_or_ui
        )
        serializer = TestCaseSerializer(test_cases, many=True)
        sheet_data = serializer.data
        column_varialble_actual_result = "Actual Result"
        column_variable_pass_or_fail = "Pass/ Fail"
        column_varialble_bug_id = "Bug ID"
        columns = [
            {"field": "test_case_id", "headerName": "Test Case ID"},
            {"field": "description", "headerName": "Test Case Description",
                "tooltipField": 'description'},
            {"field": "feature", "headerName": "Feature",
                "tooltipField": 'feature'},
            {"field": "sub_feature", "headerName": "Sub Feature",
                "tooltipField": 'sub_feature'},
            {"field": "test_steps", "headerName": "Test steps",
                "tooltipField": 'test_steps'},
            {"field": "pre_condition", "headerName": "PreCondition",
                "tooltipField": 'pre_condition'},
            {"field": "expected_results", "headerName": "Expected Result",
                "tooltipField": 'expected_results'},
            {"field": "category", "headerName": "Category",
                "tooltipField": 'category'},
            {"field": "status", "headerName": "Status"},
            {
                "headerName": "Sweep 1",
                "groupId": "Sweep 1",
                "children": [
                    {"headerName": column_varialble_actual_result,
                        "field": 'sweep1.actual_result',"tooltipField": "sweep1.actual_result"},
                    {"headerName": 'Build', 'field': 'sweep1.build',"tooltipField": "sweep1.build"},
                    {"headerName": column_variable_pass_or_fail,
                        'field': 'sweep1.sweep_status',"tooltipField": "sweep1.sweep_status"},
                    {'headerName': column_varialble_bug_id,
                        'field': 'sweep1.bug_ids',"tooltipField": "sweep1.bug_ids"},
                ],
            },
            {
                "headerName": "Sweep 2",
                "groupId": "Sweep 2 ",
                "children": [
                    {"headerName": column_varialble_actual_result,
                        "field": 'sweep2.actual_result',"tooltipField": "sweep2.actual_result"},
                    {"headerName": 'Build', 'field': 'sweep2.build',"tooltipField": "sweep2.build"},
                    {"headerName": column_variable_pass_or_fail,
                        'field': 'sweep2.sweep_status',"tooltipField": "sweep2.sweep_status"},
                    {'headerName': column_varialble_bug_id,
                        'field': 'sweep2.bug_ids',"tooltipField": "sweep2.bug_ids"},
                ],
            },
            {
                "headerName": "Sweep 3",
                "groupId": "Sweep 3",
                "children": [
                    {"headerName": column_varialble_actual_result,
                        "field": 'sweep3.actual_result',"tooltipField": "sweep3.actual_result"},
                    {"headerName": 'Build', 'field': 'sweep3.build',"tooltipField": "sweep3.build"},
                    {"headerName": column_variable_pass_or_fail,
                        'field': 'sweep3.sweep_status',"tooltipField": "sweep3.sweep_status"},
                    {'headerName': column_varialble_bug_id,
                        'field': 'sweep3.bug_ids',"tooltipField": "sweep3.bug_ids"},
                ],
            },
            {
                "headerName": "Sweep 4",
                "groupId": "Sweep 4",
                "children": [
                    {"headerName": column_varialble_actual_result,
                        "field": 'sweep4.actual_result',"tooltipField": "sweep4.actual_result"},
                    {"headerName": 'Build', 'field': 'sweep4.build',"tooltipField": "sweep4.build"},
                    {"headerName": column_variable_pass_or_fail,
                        'field': 'sweep4.sweep_status',"tooltipField": "sweep4.sweep_status"},
                    {'headerName': column_varialble_bug_id,
                        'field': 'sweep4.bug_ids',"tooltipField": "sweep4.bug_ids"},
                ],
            },

        ]
        for data in sheet_data:
            for sweep_num in range(1, 5):  
                sweep_key = f"sweep{sweep_num}"
                if sweep_key in data:
                    sweep_id = data[sweep_key]["id"]
                    bug_ids_sweep = get_bug_ids_for_sweep(sweep_id)

                    if len(bug_ids_sweep) ==0:
                        data[sweep_key]["bug_ids"] = 'Nil'
                    else:
                         data[sweep_key]["bug_ids"] = bug_ids_sweep
                    
        if len(sheet_data) == 0:
            return Response(
                report_error.EXCEL_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
            )
        sheet_data = {"rows": list(sheet_data), "columns": columns}
        return JsonResponse({"data": sheet_data})
    except CustomException as ex:
        return Response(ex.error, status=status.HTTP_400_BAD_REQUEST)


def list_and_update_sheet_validation(request):
    project_id = request.GET.get("projectid")
    sheet_name = request.GET.get("sheetname")

    if project_id == "" or project_id is None:
        raise CustomException(report_error.PROJECTID_NOT_FOUND)
    elif sheet_name is None or sheet_name == "":
        raise CustomException(report_error.SHEETNAME_NOT_FOUND)

    try:
        project_id = int(project_id)
    except ValueError:
        raise CustomException(report_error.PROJECTID_IS_NOT_INT)
    user = user_details(request)
    user_access = has_access_to_project(user.id, project_id)
    if not user_access:
        raise CustomException(project_error.PROJECT_NOT_FOUND)

    project = Projects.objects.get(pk=project_id)
    if project is None:
        raise CustomException(project_error.PROJECT_NOT_FOUND)


@api_view(["GET"])
# @user_authorization
def export_report(request, project_id):
    project_exists(project_id, logger)
    excel_file_path = export_to_excel(project_id, logger)
    return Response({"file_path": excel_file_path})


@api_view(["GET"])
@user_authorization
def severity_report(request, project_id):
    try:
        if check_project_exists(project_id, logger):
            user = user_details(request)
            if has_access_to_project(user.id, project_id):
                return fetch_severity(project_id, request, logger)
            return Response(project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
        return Response(project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(e)
        return Response(
            project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@user_authorization
def feature_wise_bug_count_report(request, project_id):
    try:
        project_exists(project_id, logger)
        user = user_details(request)
        user_access = has_access_to_project(user.id, project_id)
        if not user_access:
            return Response(
                project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
            )
        project_id = int(project_id)
        Projects.objects.get(pk=project_id)
    except Exception:
        return Response(
            project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        api_or_ui = request.GET.get('testCaseCategory')
        return feature_wise_bug_count(project_id, api_or_ui)
    except Exception:
        return INTERNAL_SERVER_ERROR


@api_view(["GET"])
@user_authorization
def feature_wise_summary_report(request, project_id):
    try:
        if check_project_exists(project_id, logger):
            user = user_details(request)
            if has_access_to_project(user.id, project_id):
                return feature_wise_summary(project_id, request, logger)
            return Response(project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
        return Response(project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        return INTERNAL_SERVER_ERROR


@api_view(["GET"])
@user_authorization
def bugs_stats(request, project_id):
    try:
        project_exists(project_id, logger)
        user = user_details(request)
        user_access = has_access_to_project(user.id, project_id)
        if not user_access:
            return Response(
                project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
            )
        project_id = int(project_id)
        Projects.objects.get(pk=project_id)
    except Exception:
        return Response(
            project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        api_or_ui = request.GET.get('testCaseCategory')
        response = stats(project_id, logger,api_or_ui)
        return response
    except Exception:
        return INTERNAL_SERVER_ERROR


@api_view(["GET"])
@user_authorization
def test_case_summary(request, project_id):
    try:
        project_exists(project_id, logger)
        user = user_details(request)
        user_access = has_access_to_project(user.id, project_id)
        if not user_access:
            return Response(
                project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
            )
        project_id = int(project_id)
        Projects.objects.get(pk=project_id)
    except Exception:
        return Response(
            project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        api_or_ui = request.GET.get('testCaseCategory')
        response = test_summary(project_id, logger,api_or_ui)
        return response
    except Exception:
        return INTERNAL_SERVER_ERROR

@api_view(["GET"])
@user_authorization
def test_progress_report(request, project_id):
    try:
        if check_project_exists(project_id, logger):
            user = user_details(request)
            if has_access_to_project(user.id, project_id):
                return test_progress(project_id, request, logger)
            return Response(project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
        return Response(project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        return INTERNAL_SERVER_ERROR
