
from rest_framework.response import Response
from report.models.test_cases import TestCases, Sweep, SweepBugs
from report.utils.fetch_severity import validate_test_case_category
from report.utils.util import fetch_model_data


def feature_wise_summary(project_id, request, logger):
    test_case_category = request.GET.get('testCaseCategory')
    category = validate_test_case_category(test_case_category)
    features_data = []

    filters = {
        'project': project_id
    }
    if category:
        filters['test_case_choice'] = category

    test_cases = fetch_model_data(TestCases, logger, filters)
    if test_cases is None:
        return Response([], status=200)

    for test_case in test_cases:
        feature_name = test_case.feature
        feature_data = next((feature for feature in features_data if feature['feature'] == feature_name), None)

        if feature_data is None:
            feature_data = {
                'feature': feature_name,
                'total_tc': 0,
                'passed_tc': 0,
                'progress': '0.00%',
                'no_of_bugs': 0,
                'detection_rate': '0.00%',
            }
            features_data.append(feature_data)

        feature_data['total_tc'] += 1

        if test_case.status.lower() == 'pass':
            feature_data['passed_tc'] += 1

        # Calculate progress
        feature_data['progress'] = f"{(feature_data['passed_tc'] / feature_data['total_tc'] * 100):.2f}%"

    for feature_data in features_data:
        # Calculate the total number of bugs with corresponding 'bug_id' in 'SweepBugs'
        sweep_data = Sweep.objects.filter(test_cases__feature=feature_data['feature'])
        total_bugs = SweepBugs.objects.filter(sweep__in=sweep_data).values('bug_id').distinct().count()
        feature_data['no_of_bugs'] += total_bugs

        # Calculate the detection rate
        feature_data['detection_rate'] = f"{(feature_data['no_of_bugs'] / feature_data['total_tc'] * 100):.2f}%"

    return Response(features_data, status=200)

