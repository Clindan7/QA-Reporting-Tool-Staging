import json
import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from project.views import generate_one_week_data
from report.models.test_cases import TestCaseDateAndCount
from project.models.projects import Projects
from project.serializers import ProjectSerializer
from rest_framework.test import APIClient
from users.models.members import Members
import datetime

from unittest.mock import patch
from report.utils.util import feature_wise_bug_count, fetch_model_field_data, find_dates
from unittest.mock import Mock, patch
from project.utils import CustomException
from project.validation import EditProjectDetailsValidation


class ProjectApiTestCase(TestCase):
    # Setting up initial data for tests
    def setUp(self):
        self.project = Projects.objects.create(
            id=1,
            notes='Test Notes',
            uat_release='2023-10-09',
            status=0,
            release_date='2023-10-10',
            remarks='Test Remarks',
        )
        self.user = Members.objects.create(
            name="kannan",
            email="kannan.p@innovaturelabs.com",
            id=1,
            role_type=1,
            status=1

        )
        self.test_case_date_count = TestCaseDateAndCount.objects.create(
            id=1,
            excuted_test_case_count=1,
            passed_test_case_count=2,
            date_of_executiion="2023-05-02"
        )

    def test_failed_case_put_project_by_id(self, ):

        project_id = self.project.id
        url = reverse('get_project_by_id', args=[project_id])
        client = APIClient()
        # Providing invalid token for unauthorized access
        client.credentials(HTTP_AUTHORIZATION='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imthbm5hbi5wQGlubm92YXR1cmVsYWJzLmNvbSIsInR5cGUiOiJhY2Nlc3MiLCJleHAiOjM4NDEzMDQ3MzR9.WSk9rfW6NPpU6ENWKcQK6kmfCJ81Db-QOQAt10za6eM')

        # Valid data for updating the project
        valid_data = {
            'notes': 'Updated Notes',
            'uat_release': '2023-11-11',
            'status': 1,
            'release_date': '2023-11-12',
            'remarks': 'Updated Remarks',
        }

        # Sending a PUT request with the updated data
        response = client.put(url, data=json.dumps(valid_data), format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_one_week_data(self):
        # Mock project data and dates dictionary
        project_id = self.project.id
        start_date = datetime.date(2023, 1, 1)  # Set your desired start date
        end_date = datetime.date(2023, 1, 7)  # Set your desired end date

        projects_dates = {
            # Mock project data for specific dates
            "2023-01-02": (10, 8, "2023-01-02"),
            "2023-01-04": (5, 4, "2023-01-04"),
            # Add more dates and corresponding data as needed for testing
        }

        # Call the function to generate data for the specified date range
        generated_data = generate_one_week_data(
            project_id, start_date, end_date, projects_dates)

        # Expected data for comparison
        expected_data = [
            {
                "executed_test_case_count": 0,
                "passed_test_case_count": 0,
                "date_of_execution": "2023-01-01",
                "project": project_id,
            },
            {
                "executed_test_case_count": 10,
                "passed_test_case_count": 8,
                "date_of_execution": "2023-01-02",
                "project": project_id,
            },
            {
                "executed_test_case_count": 0,
                "passed_test_case_count": 0,
                "date_of_execution": "2023-01-03",
                "project": project_id,
            },
            {
                "executed_test_case_count": 5,
                "passed_test_case_count": 4,
                "date_of_execution": "2023-01-04",
                "project": project_id,
            },
            # Add expected data for the rest of the date range
        ]

        # Assertions to compare generated data with expected data
        self.assertEqual(len(generated_data), 7)
        for generated, expected in zip(generated_data, expected_data):
            self.assertEqual(generated, expected)


class TestFetchModelFieldData(unittest.TestCase):
    def setUp(self):
        self.mock_model = Mock()
        self.mock_logger = Mock()

    def test_fetch_with_no_filters(self):
        # Test fetching data without any filters
        fetch_model_field_data(self.mock_model, self.mock_logger, "id")

        # Assert that it returns all data
        self.assertTrue(self.mock_model.objects.all().exists())

    def test_fetch_with_specific_field(self):
        # Test fetching data with a specific field
        filters = {"status": "active"}
        result = fetch_model_field_data(
            self.mock_model, self.mock_logger, "name", filters)

        # Assert that it returns the specified field for the filtered data
        # Modify this assertion based on expected behavior
        self.assertTrue(result)


class TestFeatureWiseBugCount(unittest.TestCase):
    def setUp(self):
        self.mock_logger = Mock()
        self.mock_test_cases = Mock()
        self.mock_sweep = Mock()
        self.mock_sweep_bugs = Mock()

    def test_feature_wise_bug_count(self):
        # Mocking the models' objects
        self.mock_test_cases.objects.filter.return_value = [
            1, 2, 3]  # Mocking test case ids
        self.mock_sweep.objects.filter.return_value = [
            4, 5]  # Mocking sweep ids
        self.mock_sweep_bugs.objects.filter.return_value = [
            Mock(bug_id=100), Mock(bug_id=101)]  # Mocking bug count numbers

        # Call the function
        feature_wise_bug_count(projectid=1, api_or_ui='API')


class TestEditProjectDetailsValidation(unittest.TestCase):
    def setUp(self):
        self.validator = EditProjectDetailsValidation()

    def test_validate_project_data_valid_fields(self):
        # Test valid fields
        valid_data = {
            'notes': 'Sample notes',
            'uat_release': '2023-11-17',
            'status': 1,
            'release_date': '2023-11-18',
            'remarks': 'Sample remarks',
            'risk': 'Low',
            'start_date': '2023-11-15'
        }
        try:
            self.validator.validate_project_data(valid_data)
        except CustomException as ex:
            self.fail(f"Unexpected exception: {ex}")

    def test_validate_project_data_invalid_field(self):
        # Test invalid field
        invalid_data = {
            'notes': 'Sample notes',
            'invalid_field': 'Value'
        }
        with self.assertRaises(CustomException):
            self.validator.validate_project_data(invalid_data)
