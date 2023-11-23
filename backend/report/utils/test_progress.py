from rest_framework.response import Response
from report.models.batch_process import BugSummary
from report.models.test_cases import TestCaseDateAndCount, TestCases
from project.models import ProjectIssues, ProjectIssueCategories, Category
from report.utils.util import fetch_model_data
from datetime import datetime, timedelta, date


def if_first_created(first_created_issue):
    if first_created_issue is None:
        return Response([], status=200)


def if_bug_summary(bug_summary_instance):
    if bug_summary_instance:
        open_bugs_value = int(bug_summary_instance.open_bugs)
    else:
        open_bugs_value = 0
    return open_bugs_value


def if_iteration(first_iteration,remaining_execution_tc,executed_test_case_count,tc_not_run_global):
    if first_iteration:
        tc_not_run = remaining_execution_tc - executed_test_case_count
    else:
        tc_not_run = tc_not_run_global - executed_test_case_count
    return tc_not_run


def test_progress(project_id, request, logger):
    try:
        open_bugs_value = 0
        test_case_category = request.GET.get('testCaseCategory')
        dates = []
        result = {"dates": dates, "categories": {}}
        filter3 = {
            'project': project_id,
            'issue_type': 'Bug',
            'projectissuecategories__category__name': test_case_category
        }

        first_created_issue = fetch_model_data(
            ProjectIssues, logger, filter3).order_by('created_in_backlog').first()
        if_first_created(first_created_issue)
        started_date = first_created_issue.created_in_backlog.date()
        current_date = date.today()
        fetched_dates = generate_date_list(started_date, current_date)
        result["dates"] = [date.strftime('%Y-%m-%d') for date in fetched_dates]

        total_tc_count = TestCases.objects.filter(
            project_id=project_id, test_case_choice=test_case_category).count()

        remaining_execution_tc = total_tc_count
        global tc_not_run_global  # Declare tc_not_run_global as a global variable

        tc_not_run_global = 0
        total_bugs_value = 0
        tc_not_run_global = 0
        first_iteration = True
        tc_not_run = 0
        for date1 in fetched_dates:
            start_datetime = datetime.combine(date1, datetime.min.time())
            end_datetime = datetime.combine(date1, datetime.max.time())
            filters = {
                'project': project_id,
                'create_date__range': (start_datetime, end_datetime),
                'test_case_choice': test_case_category
            }
            bug_summary_instance = fetch_model_data(
                BugSummary, logger, filters).first()

            open_bugs_value = if_bug_summary(bug_summary_instance)

            result["categories"]["openBugs"] = result["categories"].get(
                "openBugs", [])
            result["categories"]["openBugs"].append(open_bugs_value)
            filters = {
                'project': project_id,
                'issue_type': 'Bug',
                'created_in_backlog__date': date1,
                'projectissuecategories__category__name': test_case_category
            }

            project_issues = fetch_model_data(ProjectIssues, logger, filters)

            if project_issues:
                total_bugs_value = total_bugs_value + project_issues.count()
            result["categories"]["totalBugs"] = result["categories"].get(
                "totalBugs", [])
            result["categories"]["totalBugs"].append(total_bugs_value)

            filter4 = {
                'project': project_id,
                'test_case_choice': test_case_category,
                'date_of_executiion': date1,
            }

            projects_dates = fetch_model_data(
                TestCaseDateAndCount, logger, filter4).order_by('date_of_executiion').first()

            if projects_dates:

                executed_test_case_count = projects_dates.excuted_test_case_count
                passed_test_case_count = projects_dates.passed_test_case_count
                tc_not_run=if_iteration(first_iteration,remaining_execution_tc,executed_test_case_count,tc_not_run_global)
                tc_not_run_global = tc_not_run
                remaining_execution_tc -= passed_test_case_count

                result["categories"]['remaingTcToExecute'] = result["categories"].get(
                    'remaingTcToExecute', [])
                result["categories"]['remaingTcToExecute'].append(
                    remaining_execution_tc)
                result["categories"]['tcNotRun'] = result["categories"].get(
                    'tcNotRun', [])
                result["categories"]['tcNotRun'].append(tc_not_run_global)
                first_iteration = False

            else:
                if first_iteration:
                    tc_not_run_global = remaining_execution_tc
                    first_iteration = False
                executed_test_case_count = 0
                validate_key('tcNotRun', result)

                if tc_not_run_global > 0:
                    result["categories"]['tcNotRun'].append(tc_not_run_global)
                else:
                    result["categories"]['tcNotRun'].append(
                        executed_test_case_count)
                result["categories"]['remaingTcToExecute'] = result["categories"].get(
                    'remaingTcToExecute', [])
                result["categories"]['remaingTcToExecute'].append(
                    remaining_execution_tc)

        return Response(result, status=200)

    except Exception as e:
        print(e)
        return Response([], status=200)


def validate_key(tc_not_run, result):
    if tc_not_run not in result["categories"]:
        result["categories"]['tcNotRun'] = []


def generate_date_list(start_date, end_date):
    dates = []

    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)

    return dates
