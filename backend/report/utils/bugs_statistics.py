
from project.models.projects import ProjectIssues,ProjectIssueCategories
from report.models.test_cases import TestCases
from rest_framework.response import Response

def stats(project_id, logger, api_or_ui):
    try:
        project_issues = ProjectIssues.objects.filter(project__id=project_id,issue_type='Bug')

        if api_or_ui in ['API', 'UI']:
            project_issues = project_issues.filter(projectissuecategories__category__name=api_or_ui)

        total_bugs_reported = project_issues.count()
        open_bugs = project_issues.filter(issue_status='Open').count()
        closed_bugs = project_issues.filter(issue_status='Closed').count()
        bugs_in_progress = project_issues.filter(issue_status='In Progress').count()
        resolved_bugs = project_issues.filter(issue_status='Resolved').count()
        bugs_reported_by_client = ProjectIssueCategories.objects.filter(
            project_issues__in=project_issues,
            category__name='Bugs reported by client'
        ).count()

        response_data = {
            "total_bugs_reported": total_bugs_reported,
            "open_bugs": open_bugs,
            "closed_bugs": closed_bugs,
            "bugs_in_progress": bugs_in_progress,
            "resolved_bugs": resolved_bugs,
            "bugs_reported_by_client": bugs_reported_by_client
        }

        return Response(response_data, status=200)
    except Exception as e:
        logger.info(e)
        return Response({"message": "error calculating statistics"}, status=500)
    
def test_summary(project_id, logger, api_or_ui):
    try:
        test_cases = TestCases.objects.filter(project__id=project_id)
        if api_or_ui in ['API', 'UI']:
            test_cases = test_cases.filter(test_case_choice=api_or_ui)

        total_test_cases = test_cases.count()
        executed_test_cases = test_cases.exclude(status__in=['', 'Not Tested']).count()
        not_yet_tested = test_cases.filter(status='').count()
        passed_test_cases = test_cases.filter(status='Pass').count()
        failed_test_cases = test_cases.filter(status='Fail').count()
        not_executed_test_cases = test_cases.filter(status='Not Tested').count()
        remaining_tc_to_execute = not_yet_tested+failed_test_cases+not_executed_test_cases

        if total_test_cases == 0:
            project_progress = 0
        else:
            project_progress = (passed_test_cases / total_test_cases) * 100

        response_data = {
            "total_test_cases": total_test_cases,
            "executed_test_cases": executed_test_cases,
            "not_yet_tested": not_yet_tested,
            "passed_test_cases":passed_test_cases,
            "failed_test_cases": failed_test_cases,
            "not_executed_test_cases": not_executed_test_cases,
            "remaining_tc_to_execute":remaining_tc_to_execute,
            "project_progress": project_progress
        }
        return Response(response_data, status=200)
    except Exception as e:
        logger.info(e)
        return Response({"message": "error calculating statistics"}, status=500)
