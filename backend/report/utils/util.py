from venv import logger
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from report.models.test_cases import Sweep, SweepBugs, TestCases
from project.models import Projects
from rest_framework import status
from rest_framework.response import Response
from project import project_error
from datetime import datetime, timedelta


def fetch_model_data(model, logger, filters=None):
    if filters is None:
        filters = {}
    data = model.objects.all()

    # Apply filters based on the input dictionary
    for field, value in filters.items():
        if value:
            data = data.filter(**{field: value})

    # Check if any data is found
    if not data.exists() and any(filters.values()):
        filter_conditions = ", ".join(
            [f"{field}='{value}'" for field, value in filters.items() if value])
        logger.error(f"No data found in db for {filter_conditions}")

    return data


def fetch_model_field_data(model, logger, field_name, filters=None):
    if filters is None:
        filters = {}
    data = model.objects.all()

    # Apply filters based on the input dictionary
    for field, value in filters.items():
        if value:
            data = data.filter(**{field: value})

    # Check if any data is found
    if not data.exists() and any(filters.values()):
        filter_conditions = ", ".join(
            [f"{field}='{value}'" for field, value in filters.items() if value])
        logger.error(f"No data found in db for {filter_conditions}")

    # If field_name is provided, only fetch that specific field
    if field_name:
        data = data.values_list(field_name, flat=True)

    return data


def fetch_model_data_specific_field(model, logger, fields=None, filters=None):
    if filters is None:
        filters = {}

    # If no fields are specified, fetch all fields
    if fields is None:
        data = model.objects.all()
    else:
        data = model.objects.only(*fields)

    # Apply filters based on the input dictionary
    for field, value in filters.items():
        if value:
            data = data.filter(**{field: value})

    # Check if any data is found
    if not data.exists() and any(filters.values()):
        filter_conditions = ", ".join(
            [f"{field}='{value}'" for field, value in filters.items() if value])
        logger.error(f"No data found in db for {filter_conditions}")

    return data


def project_exists(project_id, logger):
    try:
        Projects.objects.get(id=project_id)
        logger.info("Project exists in db")
    except ObjectDoesNotExist:
        return Response(
            project_error.PROJECT_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST
        )


def check_project_exists(project_id, logger):
    exists = Projects.objects.filter(id=project_id)
    if exists:
        logger.info("Project exists in db")
        return True


def find_dates(start_date):
    # Calculate the days until the next Friday (0: Monday, 1: Tuesday, ..., 6: Sunday)
    days_until_friday = (4 - start_date.weekday()) % 7

    # Calculate the next Friday date by adding the days_until_friday to the start_date
    next_friday = start_date + timedelta(days=days_until_friday)
    print("days_until_friday-----", days_until_friday,
          '   : next_friday', next_friday)
    return next_friday
def feature_wise_bug_count(projectid, api_or_ui='API'):
    filters = {
        'project_id': projectid,
        'test_case_choice': api_or_ui
    }
    field = "feature"
    feature_list = fetch_model_field_data(TestCases, logger, field, filters)
    feature_list = list(set(feature_list))
    bug_count = {}
    
    for feature in feature_list:
        filters = {
            'project_id': projectid,
            'feature': feature,
            'test_case_choice': api_or_ui,
        }
        field = "id"
        test_case_ids = fetch_model_field_data(TestCases, logger, field, filters)
        
        unique_bug_id = set()

        for test_case_id in test_case_ids:
            filters = {
                'test_cases_id': test_case_id,
            }
            field = "id"
            sweep_ids = fetch_model_field_data(Sweep, logger, field, filters)

            for sweep_id in sweep_ids:
                bug_ids = SweepBugs.objects.filter(sweep_id=sweep_id).values('bug_id').distinct()
                unique_bug_id.update(bug['bug_id'] for bug in bug_ids)
                
        total_bug_count = len(unique_bug_id)
        bug_count[feature] = total_bug_count

    response = {"feature_wise_bug_count": bug_count}

    return Response(response)



