from rest_framework.response import Response
from project.models import ProjectIssues, Projects, ProjectIssueCategories
from report.utils.util import fetch_model_data
from datetime import datetime, timedelta, date


def validate_test_case_category(test_case_category):
    return test_case_category if test_case_category in ('API', 'UI') else None


def fetch_category_ids(project_id, category, logger):
    filters = {
        'category__name': category,
        'project_issues__project_id': project_id,
    }
    category_data = fetch_model_data(ProjectIssueCategories, logger, filters)
    return category_data.values_list('project_issues_id', flat=True)


def fetch_severity(project_id, request, logger):
    try:
        # test_case_category must be API or UI
        test_case_category = request.GET.get('testCaseCategory')
        category = test_case_category
        dates = []
        result = []
        table_priority_counts = []
        priority_levels = ['high', 'normal', 'low']
        issue_type = 'Bug'

        filter3 = {
            'project': project_id,
            'issue_type': issue_type,
        }

        # fetching created date of the first issue raised in backlog
        first_created_issue = fetch_model_data(ProjectIssues, logger, filter3).order_by('created_in_backlog').first()
        if first_created_issue is None:
            return Response([], status=200)

        started_date = first_created_issue.created_in_backlog.date()
        current_date = date.today()

        fridays = get_fridays_between_dates(started_date, current_date)
        fridays.append(current_date)
        fridays_formatted = [date.strftime('%Y-%m-%d') for date in fridays]
        dates.append(fridays_formatted)

        # table data
        total_issues_count = 0
        for priority in priority_levels:
            filters = {
                'project': project_id,
                'priority': priority,
                'issue_type': issue_type,
                'created_in_backlog__range': (started_date, current_date + timedelta(days=1)),
                'projectissuecategories__category__name': test_case_category
            }

            data = fetch_model_data(ProjectIssues, logger, filters)
            priority_count = data.count()
            total_issues_count += priority_count
            table_priority_counts.append({'priority': priority, 'count': priority_count})

        # Calculate and add the percentage to each priority count
        for item in table_priority_counts:
            item['percentage'] = (item['count'] / total_issues_count) * 100 if total_issues_count > 0 else 0

        result.append({'table_data': table_priority_counts})
        priority_counts = {}
        prev_datez = started_date
        return bugs_per_fridays(fridays, priority_levels, project_id, issue_type, prev_datez, category, logger,
                                priority_counts, result, dates)
    except Exception:
        return Response([], status=200)


def bugs_per_fridays(fridays, priority_levels, project_id, issue_type, prev_datez, category, logger, priority_counts, result, dates):
    for datez in fridays:
        end_date = datez + timedelta(days=1)
        for priority in priority_levels:
            filters = {
                'project': project_id,
                'priority': priority,
                'issue_type': issue_type,
                'created_in_backlog__range': (prev_datez, end_date),
                'projectissuecategories__category__name': category

            }

            data = fetch_model_data(ProjectIssues, logger, filters)

            if priority not in priority_counts:
                priority_counts[priority] = []

            priority_counts[priority].append(data.count())
        prev_datez = end_date

    # Convert the priority_counts dictionary into the desired format
    weekly_data = [{'priority': p, 'count': counts} for p, counts in priority_counts.items()]
    result.append({'labels': dates})
    result.append({'datasets': weekly_data})
    return Response(result, status=200)



def get_fridays_between_dates(start_date, end_date):
    fridays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 4:  # 4 represents Friday
            fridays.append(current_date)
        current_date += timedelta(days=1)  # Move to the next day
    return fridays
