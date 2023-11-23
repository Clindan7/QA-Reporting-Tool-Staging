from report.models.test_cases import TestCases
from report.models.summary import Summary
from report.models.testcase_result import TestcaseResult
from report.record_update_functions import create_test_case, process_sheet
from report.excel_utils import read_excel_file


field_mapping_summary = {
    "Module/ Feature": "feature",
    "No. of Test Cases": "number_of_testcases",
    "No. of Test Cases Executed": "executed_testcases_count",
    "No. of Test Cases Passed": "passed_testcases_count",
    "No. of Test Cases Failed": "failed_testcases_count",
    "No. of Test Cases Not tested": "not_tested_count",
}

field_mapping = {
    "Version No.": "version",
    "Date of Release": "date_of_release",
    "Prepared by": "prepared_by",
    "Reviewed by": "reviewed_by",
    "Approved by": "approved_by",
    "Change Description": "change_description",
}


def insert_cover_and_amendment(
    row, sheet_name, cover_and_version_data, amendment_of_tc_data, project_id
):
    existing_record = TestcaseResult.objects.filter(
        **row, sheet_name=sheet_name, project_id=project_id
    ).first()
    if existing_record:
        TestcaseResult.objects.filter(project_id=project_id).delete()

    if sheet_name == "Cover & Version":
        TestcaseResult.objects.create(
            **row, sheet_name=sheet_name, project_id=project_id
        )
        cover_and_version_data.append(
            dict(row, sheet_name=sheet_name, project_id=project_id)
        )
    else:
        TestcaseResult.objects.create(
            **row, sheet_name=sheet_name, project_id=project_id
        )
        amendment_of_tc_data.append(
            dict(row, sheet_name=sheet_name, project_id=project_id)
        )


def insert_summary(sheet_df, summary_data, project_id):
    process_sheet(sheet_df)
    sheet_df.rename(columns=field_mapping_summary, inplace=True)
    for row in sheet_df.to_dict(orient="records"):
        existing_record = Summary.objects.filter(**row, project_id=project_id).first()
        if existing_record:
            Summary.objects.filter(project_id=project_id).delete()
        Summary.objects.create(**row, project_id=project_id)
        summary_data.append(dict(row, project_id=project_id))


from django.db import transaction


def insert_dynamic(test_case, row_data, project_id, sweep_count, ui_or_api):
    with transaction.atomic():
        TestCases.objects.filter(
            project_id=project_id, test_case_choice=ui_or_api
        ).delete()
        for testcase, row in zip(test_case, row_data):
            test_data = TestCases.objects.filter(
                test_case_id=row["test_case_id"],
                sheet_name=row["sheet_name"],
                project_id=project_id,
                test_case_choice=ui_or_api,
            )
            if len(test_data) == 0:
                create_test_case(row, project_id, sweep_count, ui_or_api)


def data_processing(
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
    ui_or_api,
):
    for sheet_name, config in sheet_configs.items():
        skiprows = config["skiprows"]
        header_rows = config["header_rows"]

        sheet_df = read_excel_file(file_path, sheet_name, skiprows, header_rows)
        if sheet_name == "Cover & Version" or sheet_name == "Amendment of TC":
            process_sheet(sheet_df)
            sheet_df.rename(columns=field_mapping, inplace=True)
            for row in sheet_df.to_dict(orient="records"):
                insert_cover_and_amendment(
                    row,
                    sheet_name,
                    cover_and_version_data,
                    amendment_of_tc_data,
                    project_id=project_id,
                )
        elif sheet_name == "Summary":
            insert_summary(sheet_df, summary_data, project_id=project_id)
        else:
            process_sheet(sheet_df)
            sheet_df.rename(columns=dynamic_column_mapping, inplace=True)
    insert_dynamic(test_case, row_data, project_id, sweep_count, ui_or_api)
