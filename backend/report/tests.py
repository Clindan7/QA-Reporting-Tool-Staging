import json
from django.http import HttpRequest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
import pandas as pd
from report.utils.test_progress import generate_date_list, if_bug_summary, if_iteration
from users.models.members import Members
from report.utils.bugs_statistics import stats, test_summary
from report.record_update_functions import (
    create_test_case,
    fetch_bug_ids,
    process_sheet,
)
# Replace 'your_module' with the actual module name containing the function
from report.excel_utils import read_excel_file

from report.models.test_cases import TestCases
from report.utils.fetch_severity import fetch_category_ids
from users.models.members import Members
from report.views import (
    bug_id_dynamic_fetch,
    get_sheet_row_number,
    import_data_from_summary,
    map_status,
    process_test_cases,
    sweep_validation,
)
from report.utils.report_export_to_excel import module_test_case_sheet
from report.testcase_validation import testcase_validation
from report.models import Summary
from report import report_errors
from project.models import Projects, Versions, ProjectIssues, ProjectIssueCategories, Category, ProjectsMembers
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status

from datetime import datetime
from report.data_processing_function import insert_cover_and_amendment
from report.models.testcase_result import TestcaseResult
from datetime import date, timedelta

# Create your tests here.
import unittest
from unittest.mock import Mock, patch, MagicMock

from openpyxl.workbook import Workbook
import random
import string
import logging

logger = logging.getLogger(__name__)

SUB_FEATURE = "Sub Feature"
VALID_DESCRIPTION = "Valid Description"
VALID_FEATURE = "Valid Feature"
VALID_SUB_FEATURE = "Valid Sub Feature"
VALID_TEST_STEPS = "Valid Test Steps"
VALID_EXPECTED_RESULTS = "Valid Expected Results"
VALID_STATUS = "Valid Status"
ACTUAL_RESULT = "Unnamed: 15"
BUILD = "Unnamed: 16"
SWEEP_STATUS = "Unnamed: 17"
PASS_FAIL = "Pass/Fail"
ACTUAL_RESULT_VAR = "Actual Result"
EMAIL = "kannan.p@innovaturelabs.com"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDAsInR5cGUiOiJhY2Nlc3MiLCJleHAiOjIwMTU1MzMyNDR9.MYCrIC2Uf2gWNiR-ibO96EZqlBA7tc5MZ8QwUEVNGwA"
CONTENT_TYPE = 'application/json'
COVER_AND_VERSION = "cover and version"
COVER_AND_VERSIONS = "Cover & Version"
USER_DETAILS = "project.views.user_details"
ACCESS_TO_PROJECT = "report.views.has_access_to_project"
BUG_ID_1 = "Bug ID.1"
BUG_ID_2 = "Bug ID.2"
NOT_A_BUG_ID = "Not a Bug ID"
SHOULD_BE_IGNORED = "Should be ignored"


class UpdateTestCaseTest(unittest.TestCase):
    def test_process_sheet(self):
        data = {
            "date_of_release": ["01/12/2021", "15/05/2022", "20/09/2023"],
        }

        input_df = pd.DataFrame(data)

        process_sheet(input_df)

        expected_output = pd.DataFrame(
            {
                "date_of_release": ["2021-12-01", "2022-05-15", "2023-09-20"],
            }
        )

        pd.testing.assert_frame_equal(input_df, expected_output)


class ImportDataFromSummaryTestCase(TestCase):
    def test_invalid_file_format(self):
        invalid_file = SimpleUploadedFile("invalid_file.txt", b"file_content")

        client = APIClient()
        response = client.post(
            "/report/testcaseimport/", {"file": invalid_file}, format="multipart"
        )
        INVALID_FORMAT = {
            "error_code": 1204,
            "message": "Invalid file format. Please upload an Excel file",
        }

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(INVALID_FORMAT, report_errors.INVALID_FORMAT)


class TestSweepDataExtraction(unittest.TestCase):

    def test_valid_keys(self):
        # Test with valid keys present in row_data
        row_data = {
            ACTUAL_RESULT_VAR: "Pass",
            "Build": "1.0",
            PASS_FAIL: "Pass",
        }

        actual_result = row_data.get(ACTUAL_RESULT_VAR, "")
        build = row_data.get("Build", "")
        sweep_status = row_data.get(PASS_FAIL, "")

        self.assertEqual(actual_result, "Pass")
        self.assertEqual(build, "1.0")
        self.assertEqual(sweep_status, "Pass")

    def test_missing_keys(self):
        # Test with missing keys in row_data
        row_data = {
            ACTUAL_RESULT_VAR: "Pass"
            # Missing "Build" and "Pass/ Fail" keys
        }

        actual_result = row_data.get(ACTUAL_RESULT_VAR, "")
        build = row_data.get("Build", "")
        sweep_status = row_data.get("Pass/ Fail", "")

        self.assertEqual(actual_result, "Pass")
        self.assertEqual(build, "")
        self.assertEqual(sweep_status, "")


def generate_random_string(length, characters=string.ascii_letters + string.digits):
    return "".join(random.choice(characters) for _ in range(length))


class ExportToExcel(unittest.TestCase):
    def setUp(self):
        project_code = generate_random_string(8)
        backlog_project_id = generate_random_string(
            6, characters=string.digits)
        project_id = generate_random_string(6, characters=string.digits)
        user_id = generate_random_string(6, characters=string.digits)
        sample_token = TOKEN
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=sample_token)
        self.user = Members.objects.create(
            name="kannan", email=EMAIL, id=user_id, role_type=1, status=1
        )

        self.project = Projects.objects.create(
            id=project_id,
            notes="Tests Notes5",
            uat_release="2023-10-09",
            status=0,
            release_date="2023-10-10",
            remarks="Tesst Remarks1",
            project_code=project_code,
            backlog_project_id=backlog_project_id,
        )
        self.summary = Summary.objects.create(
            feature="feat 1",
            number_of_testcases=10,
            executed_testcases_count=10,
            passed_testcases_count=10,
            failed_testcases_count=0,
            not_tested_count=0,
            project=self.project,
        )
        backlog_version_id = generate_random_string(
            6, characters=string.digits)

        self.version = Versions.objects.create(
            name="v1",
            description="no description",
            start_date="2023-10-10",
            release_due_date="2023-10-10",
            backlog_version_id=backlog_version_id,
            status=1,
            project=self.project,
        )

        random_category_id = generate_random_string(
            6, characters=string.digits)
        self.category = Category.objects.create(
            name="Category 1",
            project=self.project,
            backlog_category_id=random_category_id,
            status=1,
        )

        backlog_issue_id = generate_random_string(6, characters=string.digits)
        self.project_issues = ProjectIssues.objects.create(
            issue_type="bug",
            subject="sub",
            description="des",
            issue_status="pass",
            project=self.project,
            backlog_issue_id=backlog_issue_id,
            created_in_backlog="2023-10-03",
            priority="high",
        )

        self.project_issue_category = ProjectIssueCategories.objects.create(
            project_issues=self.project_issues, category=self.category
        )

        self.testcase_report = TestcaseResult.objects.create(
            version='1',
            date_of_release='2023-10-10',
            prepared_by='tester 14',
            reviewed_by='tester 15',
            approved_by='tester 22',
            change_description='no changes',
            sheet_name=COVER_AND_VERSION,
            project=self.project
        )

        self.testcase = TestCases.objects.create(
            test_case_id="Test_1",
            description="no description",
            feature="sample feature",
            sub_feature="sample sub feature",
            test_steps="step 1",
            pre_condition="nothing",
            expected_results="expected",
            category="test category",
            status="pass",
            sheet_name="sheet4",
            project_issues=self.project_issues,
            comments="comments",
            test_case_choice='API',
            project=self.project,
        )
        self.testcase = TestCases.objects.create(
            test_case_id="Test_11",
            description="no description1",
            feature="sample feature1",
            sub_feature="sample sub feature1",
            test_steps="step 11",
            pre_condition="nothing1",
            expected_results="expected1",
            category="test category1",
            status="fail",
            sheet_name="sheet41",
            project_issues=self.project_issues,
            comments="comments1",
            test_case_choice='API',
            project=self.project,
        )
        member_id1 = generate_random_string(6, characters=string.digits)

        self.user = Members.objects.create(
            name="kannann",
            email=EMAIL,
            id=member_id1,
            role_type=1,
            status=1
        )

        self.project_member = ProjectsMembers.objects.create(
            project_id=self.project.id,
            member_id=self.user.id,
            status=1
        )

        self.cover_and_version_data = []
        self.amendment_of_tc_data = []
        self.logger = logger

    def test_create_test_case(self):
        data = {
            "test_case_id": "TC_001",
            "description": "Sample test case description",
            "feature": "Sample feature",
            "sub_feature": "Sample sub feature",
            "test_steps": "Sample test steps",
            "pre_condition": "Sample pre-condition",
            "expected_results": "Sample expected results",
            "category": "Sample category",
            "status": "pass",  # Choose from "pass" or "fail"
            "test_case_choice": "ui",  # Choose from "api" or "ui"
            "sheet_name": "Sheet1",
            # Assuming you have valid foreign key IDs for BrowserCompatibility, Projects, and ProjectIssues models
            # Replace with the valid ID from BrowserCompatibility model
            "browser_compatibility_id": 1,
            "project_id": 1,  # Replace with the valid ID from Projects model
            "project_issues_id": 1,  # Replace with the valid ID from ProjectIssues model
            "comments": "Sample comments",
        }
        project_id = self.project.id
        sweep_count = 3
        ui_or_api = "UI"

        create_test_case(data, project_id, sweep_count, ui_or_api)

    def test_export_report_project_exists(self):
        client = APIClient()
        sample_token = TOKEN
        client.credentials(HTTP_AUTHORIZATION=sample_token)

        url = reverse("export_report", args=[self.project.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_module_test_case_sheet(self):
        workbook = Workbook()
        sheet_name = "sheet4"
        module_test_case_sheet(workbook, self.project.id, sheet_name, logger)

    @patch('report.views.user_details')
    @patch(ACCESS_TO_PROJECT)
    def test_severity_report_view(self, mock_has_access_to_project, mock_user_details):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        user_id = self.user.id
        api_or_ui = 'API'
        # Replace with your desired value
        query_param = {"testCaseCategory": "API"}
        url = reverse("severity_report", args=[project_id])
        url += f'?testCaseCategory={query_param["testCaseCategory"]}'
        mock_user_details.return_value = self.user
        mock_has_access_to_project.return_value = True
        response = client.get(
            url, {'testCaseCategory': api_or_ui, 'project_id': project_id, 'user_id': user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('project.views.user_details')
    @patch(ACCESS_TO_PROJECT)
    def test_get_project_by_id(self, mock_has_access_to_project, mock_user_details):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        user_id = self.user.id

        url = reverse('get_project_by_id', args=[project_id])

        mock_user_details.return_value = self.user
        mock_has_access_to_project.return_value = True

        response = client.get(
            url, {'project_id': project_id, 'user_id': user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('report.views.user_details')
    @patch(ACCESS_TO_PROJECT)
    def test_bug_stats(self, mock_has_access_to_project, mock_user_details):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        user_id = self.user.id

        url = reverse('bugs_stats', args=[project_id])

        mock_user_details.return_value = self.user
        mock_has_access_to_project.return_value = True

        response = client.get(
            url, {'project_id': project_id, 'user_id': user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    @patch('report.views.user_details')
    @patch(ACCESS_TO_PROJECT)  
    def test_test_case_summary(self, mock_has_access_to_project, mock_user_details):
        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        user_id = self.user.id

        url = reverse('test_case_summary', args=[project_id])

        mock_user_details.return_value = self.user
        mock_has_access_to_project.return_value = True

        response = client.get(
            url, {'project_id': project_id, 'user_id': user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    @patch('report.views.user_details')
    @patch(ACCESS_TO_PROJECT)
    def test_feature_wise_bug_count_report_api_success(self, mock_has_access_to_project, mock_user_details):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        user_id = self.user.id

        url = reverse('feature_wise_bug_count_report', args=[project_id])

        mock_user_details.return_value = self.user
        mock_has_access_to_project.return_value = True

        response = client.get(
            url, {'project_id': project_id, 'user_id': user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    @patch('report.views.user_details')
    @patch(ACCESS_TO_PROJECT)
    def test_feature_wise_summary(self, mock_has_access_to_project, mock_user_details):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        user_id = self.user.id
        api_or_ui = 'API'
        # Replace with your desired value
        query_param = {"testCaseCategory": "API"}
        url = reverse("feature_wise_summary_report", args=[project_id])
        url += f'?testCaseCategory={query_param["testCaseCategory"]}'
        mock_user_details.return_value = self.user
        mock_has_access_to_project.return_value = True
        response = client.get(
            url, {'testCaseCategory': api_or_ui, 'project_id': project_id, 'user_id': user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_import_data_from_summary(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        sweep_count = 3
        api_or_ui = 'API'

        # Assuming 'file' is the name of the file input field in your API
        data = {
            # Replace with the actual file path
            'file': open('report/utils/exported_reports/ISL-ISMS-50-Test_Case_Result__Unit_TC.xlsx', 'rb'),
        }

        url = reverse("import_data_from_summary", args=[
                      project_id, sweep_count, api_or_ui])
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch('report.views.user_details')
    @patch(ACCESS_TO_PROJECT)
    def test_test_progress_report(self, mock_has_access_to_project, mock_user_details):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=TOKEN)
        project_id = self.project.id
        user_id = self.user.id
        api_or_ui = 'API'
        # Replace with your desired value
        query_param = {"testCaseCategory": "API"}
        url = reverse("test_progress_report", args=[project_id])
        url += f'?testCaseCategory={query_param["testCaseCategory"]}'
        mock_user_details.return_value = self.user
        mock_has_access_to_project.return_value = True
        response = client.get(
            url, {'testCaseCategory': api_or_ui, 'project_id': project_id, 'user_id': user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_category_ids(self):
        project_issue_category = ProjectIssueCategories.objects.create(
            project_issues=self.project_issues,
            category=self.category,
        )
        project_issue_category.save()
        category_ids = fetch_category_ids(
            self.project.id, self.category.name, logger)
        self.assertIn(project_issue_category.project_issues_id, category_ids)
        project_issue_category.delete()

    def test_insert_cover_data(self):
        row = {
            "version": 1.0,
            "date_of_release": datetime.now(),
            "prepared_by": "John Doe",
            "reviewed_by": "Jane Smith",
            "approved_by": "Alice Johnson",
            "change_description": "Bug fixes",
        }
        sheet_name = COVER_AND_VERSIONS

        insert_cover_and_amendment(
            row,
            sheet_name,
            self.cover_and_version_data,
            self.amendment_of_tc_data,
            self.project.id,
        )

        # Check if the record is inserted into the database
        record = TestcaseResult.objects.filter(
            sheet_name=sheet_name, project_id=self.project.id
        ).first()
        self.assertIsNotNone(record)

        # Check if the data is added to the appropriate data list
        self.assertIn(
            dict(row, sheet_name=sheet_name, project_id=self.project.id),
            self.cover_and_version_data,
        )

    def test_insert_amendment_data(self):
        row = {
            "version": 1.1,
            "date_of_release": datetime.now(),
            "prepared_by": "John Doe",
            "reviewed_by": "Jane Smith",
            "approved_by": "Alice Johnson",
            "change_description": "New feature added",
        }
        sheet_name = "Amendment of TC"

        insert_cover_and_amendment(
            row,
            sheet_name,
            self.cover_and_version_data,
            self.amendment_of_tc_data,
            self.project.id,
        )

        # Check if the record is inserted into the database
        record = TestcaseResult.objects.filter(
            sheet_name=sheet_name, project_id=self.project.id
        ).first()
        self.assertIsNotNone(record)

        # Check if the data is added to the appropriate data list
        self.assertIn(
            dict(row, sheet_name=sheet_name, project_id=self.project.id),
            self.amendment_of_tc_data,
        )

    def test_stats(self):
        # Mocking the necessary database models and objects
        mock_project_issues = Mock()
        mock_project_issues.filter.return_value = mock_project_issues
        mock_project_issues.count.return_value = 10

        mock_project_issue_categories = Mock()
        mock_project_issue_categories.filter.return_value = mock_project_issue_categories
        mock_project_issue_categories.count.return_value = 5

        with unittest.mock.patch('project.models.projects.ProjectIssues', mock_project_issues), \
                unittest.mock.patch('project.models.projects.ProjectIssueCategories', mock_project_issue_categories):
            response = stats(1, self.logger, "API")

        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your expected response_data values

    def test_test_summary(self):
        # Mocking the necessary database models and objects
        mock_test_cases = Mock()
        mock_test_cases.filter.return_value = mock_test_cases
        mock_test_cases.count.return_value = 20
        mock_test_cases.exclude.return_value = mock_test_cases

        with unittest.mock.patch('report.models.test_cases.TestCases', mock_test_cases):
            response = test_summary(1, self.logger, "API")

        self.assertEqual(response.status_code, 200)

    def test_new_sheet_name(self):
        row_sheet = {}
        sheet_name = "Sheet1"
        result = get_sheet_row_number(row_sheet, sheet_name)
        self.assertEqual(result, 1)

    def test_existing_sheet_name(self):
        row_sheet = {"Sheet1": 5, "Sheet2": 3}
        sheet_name = "Sheet1"
        result = get_sheet_row_number(row_sheet, sheet_name)
        self.assertEqual(result, 5)

    def test_multiple_sheets(self):
        row_sheet = {"Sheet1": 2, "Sheet2": 7}
        sheet_name = "Sheet2"
        result = get_sheet_row_number(row_sheet, sheet_name)
        self.assertEqual(result, 7)


class UpdateExcelSheetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # You may need to set up your project and other required data here.

        self.user = Members.objects.create(
            name="kannan", email=EMAIL, id=1, role_type=1, status=1
        )

        self.project = Projects.objects.create(
            id=1,
            notes="Tests Notes1",
            uat_release="2023-10-09",
            status=0,
            release_date="2023-10-10",
            remarks="Tesst Remarks8",
            project_code="ascd",
            backlog_project_id=122,
        )

        sample_token = TOKEN
        self.client.credentials(HTTP_AUTHORIZATION=sample_token)


class GetExcelSheetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # You may need to set up your project and other required data here.

        self.user = Members.objects.create(
            name="kannan", email=EMAIL, id=1, role_type=1, status=1
        )
        self.project = Projects.objects.create(
            id=1,
            notes="Tests Notes1",
            uat_release="2023-10-09",
            status=0,
            release_date="2023-10-10",
            remarks="Tesst Remarks9",
            project_code=125,
            backlog_project_id=123,
        )
        self.testcase_report = TestcaseResult.objects.create(
            version='1',
            date_of_release='2023-10-10',
            prepared_by='tester 12',
            reviewed_by='tester 11',
            approved_by='tester 223',
            change_description='no changes',
            sheet_name=COVER_AND_VERSION,
            project=self.project
        )

        sample_token = TOKEN
        self.client.credentials(HTTP_AUTHORIZATION=sample_token)

    @patch(USER_DETAILS, return_value=True)
    @patch(USER_DETAILS)
    def test_get_sheet_name(self, mock_user_details, mock_has_access_to_project):
        project_id = 1  # Replace with a valid project_id

        # Create a mock user object
        mock_user = MagicMock(name="kannan", email=EMAIL,
                              id=1, role_type=1, status=1)

        mock_user_details.return_value = mock_user

        # Pass the 'sheetname' and 'projectid' in query parameters
        url = reverse("list_all_page_name") + f"?projectid={project_id}"

        response = self.client.get(url, content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_valid_data(self):
        # Mock Projects.objects.get to return a project
        project_id = 1
        project = Projects(id=project_id)
        with patch("project.views.Projects.objects.get", return_value=project):
            request = HttpRequest()
            request.method = "POST"
            request.FILES["file"] = MagicMock(name="valid_file.xlsx")
            request.FILES["file"].name.endswith.return_value = True
            response = import_data_from_summary(request, project_id, 3, "UI")
            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)


def extract_data_from_dict(row_data):
    test_case_id = row_data.get("test_case_id", "")
    description = row_data.get("description", "")
    feature = row_data.get("feature", "")
    sub_feature = row_data.get("sub_feature", "")
    test_steps = row_data.get("test_steps", "")
    expected_results = row_data.get("expected_results", "")
    status = row_data.get("status", "")
    comments = row_data.get("comments", "")

    return (
        test_case_id,
        description,
        feature,
        sub_feature,
        test_steps,
        expected_results,
        status,
        comments,
    )


class TestExtractDataFromDict(unittest.TestCase):
    def test_extract_data_from_dict(self):
        # Sample data in the form of a dictionary
        row_data = {
            "test_case_id": "TC001",
            "description": "Test case description",
            "feature": "Feature 1",
            "sub_feature": "Sub-feature 1",
            "test_steps": "Step 1, Step 2",
            "expected_results": "Expected result 1",
            "status": "Pass",
            "comments": "No comments",
        }

        # Call the function to extract data from the dictionary
        (
            test_case_id,
            description,
            feature,
            sub_feature,
            test_steps,
            expected_results,
            status,
            comments,
        ) = extract_data_from_dict(row_data)

        # Assert that the extracted values match the expected values
        self.assertEqual(test_case_id, "TC001")
        self.assertEqual(description, "Test case description")
        self.assertEqual(feature, "Feature 1")
        self.assertEqual(sub_feature, "Sub-feature 1")
        self.assertEqual(test_steps, "Step 1, Step 2")
        self.assertEqual(expected_results, "Expected result 1")
        self.assertEqual(status, "Pass")
        self.assertEqual(comments, "No comments")


class TestTestCaseValidation(unittest.TestCase):
    def test_valid_input(self):
        # Sample valid input data
        test_case_id = "TC_001"
        feature = "Login"
        row_number = 1
        sheet_name = "TestCases"
        status = "Pass"

        error_dict = {}
        result = testcase_validation(
            test_case_id,
            feature,
            status,
            row_number,
            sheet_name,
            error_dict,
        )

        # Assert that the result should be None as there are no errors in the input
        self.assertIsNone(result)
        # Assert that the error_dict remains empty for valid input
        self.assertDictEqual(error_dict, {})


class FeatureWiseBugCountReportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # You may need to set up your project and other required data here.

        self.user = Members.objects.create(
            name="kannann", email=EMAIL, id=1, role_type=1, status=1
        )
        self.project = Projects.objects.create(
            id=1,
            notes="Tests Notese1",
            uat_release="2023-10-05",
            status=0,
            release_date="2023-10-15",
            remarks="Tesst Remarks9",
            project_code=124,
            backlog_project_id=121,
        )
        self.testcase_report = TestcaseResult.objects.create(
            version="1",
            date_of_release="2023-10-11",
            prepared_by="tester 16",
            reviewed_by="tester 17",
            approved_by="tester 225",
            change_description="no changess",
            sheet_name=COVER_AND_VERSION,
            project=self.project,
        )
        self.project_member = ProjectsMembers.objects.create(
            project_id=1,
            member_id=1,
            status=1
        )
        sample_token = TOKEN
        self.client.credentials(HTTP_AUTHORIZATION=sample_token)

    

    def test_sweep_validation_no_fail_status(self):
        # Test when bug_ids have "Fail" status but no bug ID provided
        bug_ids = ["Pass", "", "", ""]
        sheet_name = "TestSheet"
        row_number = 1

        error_dict = sweep_validation(bug_ids, row_number, sheet_name)

        expected_error_dict = {}
        self.assertEqual(error_dict, expected_error_dict)

    def test_sweep_validation_valid_bug_id(self):
        # Test when bug_ids have "Fail" status and a valid bug ID is provided
        bug_ids = ["Fail", "BUG123", "", ""]
        sheet_name = "TestSheet"
        row_number = 1

        error_dict = sweep_validation(bug_ids, row_number, sheet_name)

        expected_error_dict = {}
        self.assertEqual(error_dict, expected_error_dict)

    def test_map_status_with_status_column(self):
        # Test when the row_data has a status column
        row_data = {"ID": 1, "Name": "Test", "Status": "Open"}

        status_column_key = map_status(row_data)

        expected_status_column_key = "Status"
        self.assertEqual(status_column_key, expected_status_column_key)

    def test_map_status_without_status_column(self):
        # Test when the row_data does not have a status column
        row_data = {"ID": 1, "Name": "Test"}

        status_column_key = map_status(row_data)

        expected_status_column_key = None
        self.assertEqual(status_column_key, expected_status_column_key)

    def test_map_status_multiple_columns_with_status(self):
        # Test when there are multiple columns with "status" in their names
        row_data = {"ID": 1, "Name": "Test",
                    "Status": "Open", "Bug_Status": "New"}

        status_column_key = map_status(row_data)

        expected_status_column_key = "Status"
        self.assertEqual(status_column_key, expected_status_column_key)

    def test_bug_id_dynamic_fetch_with_bug_ids(self):
        # Test when dynamic_column_mapping has a Bug ID column
        dynamic_column_mapping = {"Bug ID 1": "A", "Bug ID 2": "B"}
        row_data = {"A": "BUG123", "B": "BUG456"}
        bug_ids_row = []

        result = bug_id_dynamic_fetch(
            dynamic_column_mapping, row_data, bug_ids_row)

        expected_bug_ids_row = ["BUG123", "BUG456"]
        self.assertEqual(result, expected_bug_ids_row)

    def test_bug_id_dynamic_fetch_without_bug_ids(self):
        # Test when dynamic_column_mapping does not have a Bug ID column
        dynamic_column_mapping = {"Other Column": "A", "Another Column": "B"}
        row_data = {"A": "Value1", "B": "Value2"}
        bug_ids_row = []

        result = bug_id_dynamic_fetch(
            dynamic_column_mapping, row_data, bug_ids_row)

        expected_bug_ids_row = []
        self.assertEqual(result, expected_bug_ids_row)

    def test_generate_date_list(self):
        # Mock the necessary data
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 5)

        # Call the function
        result = generate_date_list(start_date, end_date)

        # Assertions
        expected_result = [date(2023, 1, 1), date(2023, 1, 2), date(
            2023, 1, 3), date(2023, 1, 4), date(2023, 1, 5)]
        self.assertEqual(result, expected_result)

    def test_fetch_bug_ids(self):
        # Test case 1: Bug ID.0
        data_1 = {"Bug ID.0": "123, 456, 789"}
        assert fetch_bug_ids(data_1) == [
            "sweep1_123", "sweep1_456", "sweep1_789"]

        # Test case 2: Bug ID.1.1
        data_2 = {"Bug ID.1.1": "321, 654, 987"}
        assert fetch_bug_ids(data_2) == [
            "sweep2_321", "sweep2_654", "sweep2_987"]

        # Test case 3: Bug ID.2.2
        data_3 = {"Bug ID.2.2": ""}
        assert fetch_bug_ids(data_3) == []

        # Test case 4: Bug ID.3.3
        data_4 = {"Bug ID.3.3": 999}
        assert fetch_bug_ids(data_4) == ["sweep4_999"]

        # Test case 5: Unknown sweep
        data_5 = {"Bug ID.4.4": "111, 222, 333"}
        assert fetch_bug_ids(data_5) == [
            "unknown_sweep_111", "unknown_sweep_222", "unknown_sweep_333"]

        # Test case 6: Mixed types
        data_6 = {"Bug ID.5.5": "777, 888, 999", "Bug ID.6.6": 555}
        assert fetch_bug_ids(data_6) == [
            "unknown_sweep_777", "unknown_sweep_888", "unknown_sweep_999", "unknown_sweep_555"]

        # Test case 7: Empty data
        data_7 = {}
        assert fetch_bug_ids(data_7) == []

    def test_bug_summary_instance_not_none(self):
        class BugSummary:
            def __init__(self, open_bugs):
                self.open_bugs = open_bugs

        bug_summary = BugSummary(open_bugs=5)
        result = if_bug_summary(bug_summary)
        self.assertEqual(result, 5)  # Expected result when bug_summary_instance is not None

    def test_bug_summary_instance_none(self):
        result = if_bug_summary(None)
        self.assertEqual(result, 0)  # Expected result when bug_summary_instance is None

    def test_first_iteration_true(self):
        remaining_tc = 50
        executed_count = 20
        global_not_run = 100
        result = if_iteration(True, remaining_tc, executed_count, global_not_run)
        self.assertEqual(result, 30)  # Expected result when first_iteration is True

    def test_first_iteration_false(self):
        executed_count = 50
        global_not_run = 100
        result = if_iteration(False, 0, executed_count, global_not_run)
        self.assertEqual(result, 50)  # Expected result when first_iteration is False


class TestReadExcelFile(unittest.TestCase):

    def test_read_excel_file(self):
        file_path = "files/ISL-ISMS-50-Test_Case_Result_QA_Report_tool_API_Unit_TC.xlsx"
        sheet_name = COVER_AND_VERSIONS
        skiprows = 14
        header_rows = 1

        result_df = read_excel_file(
            file_path, sheet_name, skiprows, header_rows)

        expected_data = {
            'TC_01': {
                'Test Case Description': 'Verify that the success response is returned when API receives valid details',
                'Test Case Name': 'Access Token Generation From Refresh Token',
                'Test Data': 'Valid details',
                'Steps': '1.Open postman\n2.Enter valid url:Endpoint/use...\nHTTP status code: 200\n{\n"Refresh_Token": "ey...',
                'Expected Result': 'Untested',
                'Actual Result': 'two',
                'Build': 'two',
                'Pass/ Fail': 'two',
                'Bug ID': 'yummy'
            },
            'TC_02': {
                'Test Case Description': 'Verify that error message is returned when API receives invalid access token',
                'Test Case Name': 'Access Token Generation From Refresh Token',
                'Test Data': 'Access token',
                'Steps': '1.Open postman\n2.Enter valid url:Endpoint/use...\n{\n    "errorcode": 1003,\n    "message": "tok...',
                'Expected Result': 'Untested',
                'Actual Result': 'two',
                'Build': 'two',
                'Pass/ Fail': 'two',
                'Bug ID': 'yummy'
            }}
        expected_df = pd.DataFrame(expected_data)

        self.assertFalse(result_df.equals(expected_df))


if __name__ == '__main__':
    unittest.main()
