from datetime import date, timedelta
import jwt
import logging
from report.models.test_cases import TestCaseDateAndCount
from core import settings
from project.models.projects import Projects, ProjectsMembers, ProjectIssues
from project.serializers import ProjectSerializer
from project import project_error
from report.utils.util import fetch_model_data
from users.authorize import user_authorization
from project.validation import EditProjectDetailsValidation, EditTestCaseExecutionCount
from users.models.members import Members
from project.utils import CustomException
from urllib.parse import unquote
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .pagination import PropertyListPagination
from django.db.models import Q

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"



@api_view(["GET"])
@user_authorization
def list_projects(request):
    paginator = PropertyListPagination()
    paginator.page_size = 10

    search_query = unquote(request.GET.get("search", ""))
    status_filter = request.GET.get("status", "")

    user_info = request.user_info
    user_id = user_info.get("id")
    try:
        projects = (
            ProjectsMembers.objects.filter(member__id=user_id)
            .values_list(
                "project__id",
                "project__name",
                "project__project_code",
                "project__notes",
                "project__release_date",
                "project__status",
                "project__backlog_project_id",
                "project__create_date",
                "project__update_date",
                "project__risk",

            )
            .distinct()
        )
        updated_projects = []
        for project in projects:
            filters = {
                'project': project[0],
                'issue_type': 'Bug',
                'issue_status': 'Closed'
            }
            closed_issue_count = fetch_model_data(ProjectIssues, logger, filters).count()

            filters = {
                'project': project[0],
                'issue_type': 'Bug'
            }
            total_issue_count = fetch_model_data(ProjectIssues, logger, filters).count()

            project_issue_count = total_issue_count - closed_issue_count

            updated_projects.append(
                (*project[:-1], project_issue_count, project[-1])
            )

        if status_filter:
            if status_filter not in ["0", "1"]:
                return Response(
                    {
                        "errorcode": 1017,
                        "message": "Invalid status value. Status must be 0 or 1.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            updated_projects = filter(
                lambda x: x[5] == int(status_filter), updated_projects
            )

        updated_projects = sorted(
            updated_projects,
            key=lambda x: (
                0 if x[10] and str(x[10]).strip() else 1,
                x[4],
            ),
            reverse=False,
        )

        if search_query:
            updated_projects = [
                project for project in updated_projects if search_query.lower() in project[1].lower()
            ]

        paginated_projects = paginator.paginate_queryset(
            updated_projects, request)

        project_data = [
            {
                "id": project[0],
                "name": project[1],
                "projectcode": project[2],
                "notes": project[3],
                "release_date": project[4],
                "status": project[5],
                "backlog_project_id": project[6],
                "create_date": project[7],
                "update_date": project[8],
                "risk": project[10],
                "issue_count": project[9],  # Adjust index to match the correct position of project_issue_count
            }
            for project in paginated_projects
        ]

        return paginator.get_paginated_response(project_data)

    except Projects.DoesNotExist:
        return Response(
            {project_error.PROJECT_NOT_FOUND}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET", "PUT"])
@user_authorization
def get_project_by_id(request, id):
    try:
        user = user_details(request)
        user_access = has_access_to_project(user.id, id)
        if not user_access:
            return Response(
                project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
            )
        project_id = int(id)
        project = Projects.objects.get(pk=project_id)
    except Exception:
        return Response(
            project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if request.method == "GET":
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        elif request.method == "PUT":
            data = clean_request_data(request.data)

            try:
                project_validation = EditProjectDetailsValidation()
                project_validation.validate_project_data(request.data)
            except CustomException as ex:
                return Response(ex.error, status=status.HTTP_400_BAD_REQUEST)
            remark_required_or_not = remark_required_or_not_checking(
                request.data, project
            )
            if remark_required_or_not == True and "remarks" not in data:
                return Response(
                    project_error.REMARKS_REQUIRED, status=status.HTTP_400_BAD_REQUEST
                )

            user = user_details(request)
            data["updated_by"] = user.id
            serializer = ProjectSerializer(project, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "project updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(
            "Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def user_details(request):
    token = request.headers["Authorization"]
    decode = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decode["id"]
    member = Members.objects.get(id=user_id)
    return member


def clean_request_data(data):
    return {
        key: str(value).strip() if isinstance(value, str) else value
        for key, value in data.items()
    }


def remark_required_or_not_checking(data, project):
    # Check if 'remarks' is required
    remark_required = False
    if "release_date" in data:
        current_release_date = project.release_date
        new_release_date = data["release_date"]
        release_date_change = new_release_date == str(current_release_date)
        if release_date_change == True:
            remark_required = True
    if "status" in data and project.status == 0 and data["status"] == 1:
        remark_required = True

    return remark_required


def has_access_to_project(member_id, project_id):
    try:
        ProjectsMembers.objects.get(member_id=member_id, project_id=project_id)
        return True
    except ProjectsMembers.DoesNotExist:
        return False


def get_start_and_end_date(date_input=None):
    if not date_input:
        date_input = date.today()
    start_date = date_input - timedelta(days=date_input.weekday())
    # check the date exist less than start_date

    end_date = start_date + timedelta(days=6)
    return start_date, end_date


def generate_one_week_data(project_id, start_date, end_date, projects_dates):
    delta = timedelta(days=1)
    result_array = []
    while start_date <= end_date:
        date_string = start_date.strftime(DATE_FORMAT)
        data = {"executed_test_case_count": 0,
                "passed_test_case_count": 0,
                "date_of_execution": date_string,
                "project": project_id,
                }
        if date_string in projects_dates.keys():
            data = {
                "executed_test_case_count": projects_dates.get(date_string, 0)[0],
                "passed_test_case_count": projects_dates.get(date_string, 0)[1],
                "date_of_execution": projects_dates.get(date_string, date_string)[2],
                "project": project_id,
            }
        result_array.append(data)
        start_date += delta
    return result_array


@api_view(["GET"])
def get_testcase_count_and_date(request, id):
    if request.method == "GET":
        api_or_ui = request.query_params.get('testCaseCategory')
        full_projects_executed_data = {}
        result_array_old = []
        # Get the current date
        projects_dates = TestCaseDateAndCount.objects.filter(project_id=id, test_case_choice=api_or_ui).order_by(
            "date_of_executiion"
        )
        start_date, end_date = get_start_and_end_date()

        previous_dates = []
        for item in projects_dates:
            if start_date > item.date_of_executiion:
                previous_dates.append(item.date_of_executiion)
            full_projects_executed_data[item.date_of_executiion.strftime(DATE_FORMAT)] = (
                item.excuted_test_case_count, item.passed_test_case_count,
                item.date_of_executiion.strftime(DATE_FORMAT))
        result_array_today = generate_one_week_data(
            id, start_date, end_date, full_projects_executed_data)
        # generate the one week data on today
        week_data = {}
        start_date_list = []
        for idx, item in enumerate(previous_dates):
            start_date, end_date = get_start_and_end_date(item)
            if start_date in start_date_list:
                continue
            result_array_old = generate_one_week_data(
                id, start_date, end_date, full_projects_executed_data)
            week_data[f"week-{idx + 1}"] = result_array_old
            start_date_list.append(start_date)
        return Response({"today": result_array_today, "previous": week_data})


@api_view(["POST"])
@user_authorization
def update_testcase_count_and_date(request, id):
    try:
        api_or_ui = request.query_params.get('testCaseCategory')
        data = request.data

        # Validate each item in the array

        for item_data in data:
            data_validation = EditTestCaseExecutionCount()
            data = clean_request_data(item_data)
            data_validation.validate_data_types(item_data)
            test_case_count_and_executed_date = TestCaseDateAndCount.objects.filter(
                project_id=id, date_of_executiion=item_data["date_of_execution"], test_case_choice=api_or_ui)
            if len(test_case_count_and_executed_date) == 0:
                data = {
                    'excuted_test_case_count': item_data.get('executed_test_case_count', 0),
                    'passed_test_case_count': item_data.get('passed_test_case_count', 0),
                    'date_of_executiion': item_data.get('date_of_execution', ''),
                    'project_id': item_data.get('project', ''),
                    'test_case_choice': api_or_ui
                }
                TestCaseDateAndCount.objects.create(**data)
            else:

                # Update the existing entry with the new data
                existing_entry = test_case_count_and_executed_date[0]
                existing_entry.excuted_test_case_count = item_data.get('executed_test_case_count',
                                                                       existing_entry.excuted_test_case_count)
                existing_entry.passed_test_case_count = item_data.get('passed_test_case_count',
                                                                      existing_entry.passed_test_case_count)
                existing_entry.save()
        return Response({"message": "success"})

    except CustomException as ex:
        return Response(ex.error, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
