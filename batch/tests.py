import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from unittest.mock import ANY, call, MagicMock
from unittest.mock import Mock, patch
import pytest
import requests
import main
import config
import utils

BACKLOG_API_KEY = os.environ.get("BACKLOG_API_KEY")
BACKLOG_BASE_URL = os.environ.get("BACKLOG_BASE_URL")
MAIN_REQUEST_GET = 'main.requests.get'
main.logger = Mock()


def test_db_connection():
    connection = main.create_db_connection()
    assert connection is not None


def test_cursor_creation():
    connection = main.create_db_connection()
    cursor = connection.cursor()
    assert cursor is not None


def test_get_project():
    connection = main.create_db_connection()
    cursor = connection.cursor()
    project_id = 116639
    result = main.get_project(cursor, project_id)
    assert result is not None


def test_config_variables():
    assert config.BACKLOG_API_KEY is not None
    assert config.BACKLOG_BASE_URL is not None
    assert config.API_KEY is not None
    assert config.SPACE_KEY is not None


def test_insert_project():
    connection = main.create_db_connection()
    cursor = connection.cursor()

    # Test data
    project = {
        "name": "Test Project",
        "id": 11111,
        "key": "TP"
    }
    created_date = updated_date = "2023-10-10"
    main.insert_project(cursor, project, created_date, updated_date)


@patch(MAIN_REQUEST_GET)
def test_get_all_project_users(mock_requests_get):
    # Prepare mock response from requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "userId": "user1",
            "name": "User 1",
            "roleType": 1,
            "mailAddress": "user1@example.com"
        },
        {
            "id": 2,
            "userId": "user2",
            "name": "User 2",
            "roleType": 2,
            "mailAddress": "user2@example.com"
        }
    ]
    mock_requests_get.return_value = mock_response

    connection = main.create_db_connection()
    cursor = connection.cursor()
    project_id = 116639
    result = main.get_all_project_users(cursor, project_id)
    assert result is not None
    mock_requests_get.assert_called_once()


@patch(MAIN_REQUEST_GET)
def test_get_all_category(mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "projectId": 116639,
            "name": "Category 1"
        },
        {
            "id": 2,
            "projectId": 116639,
            "name": "Category 2"
        }
    ]
    mock_requests_get.return_value = mock_response
    # Mock the database cursor
    mock_cursor = Mock()
    # Mock the behavior of category_exists to return False
    main.category_exists = Mock(return_value=False)
    # Mock the behavior of insert_category
    main.insert_category = Mock()
    # Call the get_all_category function
    project_id = 116639
    result = main.get_all_category(cursor=mock_cursor, project_id=project_id)

    # Assertions
    assert result == [
        {
            'id': 1,
            'projectId': 116639,
            'name': 'Category 1'
        },
        {
            'id': 2,
            'projectId': 116639,
            'name': 'Category 2'
        }
    ]
    mock_requests_get.assert_called_once_with(
        f'{BACKLOG_BASE_URL}api/v2/projects/{project_id}/categories',
        params={"apiKey": BACKLOG_API_KEY}
    )
    # main.category_exists.assert_called_once_with(mock_cursor, 1)
    main.category_exists.assert_called_with(mock_cursor, 2)
    main.insert_category.assert_called_with(
        mock_cursor,
        {
            'id': 2,
            'projectId': 116639,
            'name': 'Category 2'
        },
        ANY,
        ANY
    )


@patch(MAIN_REQUEST_GET)
def test_get_all_versions(mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    date = "2023-10-10T00:00:00Z"
    mock_response.json.return_value = [
        {
            "id": 1,
            "projectId": 116639,
            "name": "Version 1",
            "startDate": date,
            "releaseDueDate": date,
            "description": "descrption is good"
        },
        {
            "id": 2,
            "projectId": 116639,
            "name": "Version 2",
            "startDate": date,
            "releaseDueDate": date,
            "description": "descrption is v good"
        }
    ]
    mock_requests_get.return_value = mock_response
    # Mock the database cursor
    mock_cursor = Mock()
    # Mock the behavior of project_version_exists to return False
    main.project_version_exists = Mock(return_value=False)
    # Mock the behavior of insert_version
    main.insert_version = Mock()
    # Call the get_all_versions function
    project_id = 116639
    result = main.get_all_versions(cursor=mock_cursor, project_id=project_id)
    # Assertions
    assert result == [
        {
            'backlog_version_id': 1,
            'project_id': 116639,
            'name': 'Version 1',
            'start_date': date,
            'description': 'descrption is good',
            'release_due_date': date,
        },
        {
            'backlog_version_id': 2,
            'project_id': 116639,
            'name': 'Version 2',
            'start_date': date,
            'description': 'descrption is v good',
            'release_due_date': date,

        }
    ]
    mock_requests_get.assert_called_once_with(
        f'{BACKLOG_BASE_URL}api/v2/projects/{project_id}/versions',
        params={"apiKey": BACKLOG_API_KEY}
    )
    # Check for the calls to project_version_exists with the specific arguments
    mock_version_exists_calls = [
        call(mock_cursor, 1),
        call(mock_cursor, 2),
    ]
    main.project_version_exists.assert_has_calls(mock_version_exists_calls)
    main.insert_version.assert_called_with(
        mock_cursor,
        {
            'backlog_version_id': 2,
            'project_id': 116639,
            'name': 'Version 2',
            'start_date': date,
            'description': 'descrption is v good',
            'release_due_date': date,
        },
        ANY,
        ANY,
    )


# Set create_date and update_date to the same value
common_date = datetime(2023, 10, 10, 15, 57, 22, 872624)
create_date = common_date
update_date = common_date


@patch('main.get_project')
def test_insert_version(mock_get_project):
    # Mock get_project to return a known projectId
    mock_get_project.return_value = 123
    # Create a mock cursor with a mocked execute method
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = (123,)
    # Define the input data (version and dates)
    version = {
        'project_id': 456,
        'backlog_version_id': 789,
        'name': 'Test Version',
        'description': 'Test Description',
        'start_date': '2023-01-01',
        'release_due_date': '2023-02-01',
    }
    create_date1 = '2023-03-01'
    update_date1 = '2023-03-02'
    # Call the insert_version method
    utils.insert_version(mock_cursor, version, create_date1, update_date1)
    # Define the expected SQL query and data
    expected_query = (
        "INSERT INTO versions ( project_id, backlog_version_id, name, description, start_date, "
        "release_due_date, create_date, update_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    expected_data = (
        123, 789, 'Test Version', 'Test Description', '2023-01-01', '2023-02-01', '2023-03-01', '2023-03-02', 1)
    # Check if cursor.execute was called with the expected query and data
    mock_cursor.execute.assert_called_with(expected_query, expected_data)


def test_get_all_issue_count(mocker):
    # Mock the logger to avoid any actual logging
    mocker.patch('main.logger')
    # Mock the check_backlog_api function (assuming it's defined in your 'utils' module)
    mocker.patch('main.check_backlog_api')
    # Mock requests.get to return a custom response
    mock_response = Mock()
    mock_response.json.return_value = {'count': 42}
    mocker.patch('requests.get', return_value=mock_response)
    # Mock the update_issue_count function
    project_id = 1
    # Call the function to be tested
    main.get_all_issue_count( project_id)


@patch(MAIN_REQUEST_GET)
def test_all_issues_in_a_project(mock_requests_get):
    # Prepare mock response for issues
    mock_response_issues = Mock()
    mock_response_issues.status_code = 200
    connection = main.create_db_connection()
    cursor = connection.cursor()
    mock_response_issues.json.return_value = [
        {
            'issueType': {'name': 'Bug'},
            'summary': 'Issue 1',
            'description': 'Description 1',
            'status': {'name': 'Open'},
            'assignee': {'id': 1},
            'priority': {'name': 'High'},
            'createdUser': {'id': 2},
            'milestone': [{'name': 'Milestone 1'}],
            'category': [{'id': 3}],
            'versions': [{'id': 4}],
            'startDate': '2023-10-10',
            'dueDate': '2023-10-15',
            'estimatedHours': 5.0,
            'actualHours': 3.0,
            'projectId': 116639,
            'issueKey': 'ABC-123',
            'updatedUser': {'id': 5},
            'updated': '2023-10-12T14:30:00Z',
            'id': 1001,
            'resolution': 'Fixed',
            'parentIssueId': None,
            'created': '2023-10-10T10:30:00Z',
            'customFields': [],
            'releaseDueDate': '2023-10-20'
        },
        {
            'issueType': {'name': 'Task'},
            'summary': 'Issue 2',
            'description': 'Description 2',
            'status': {'name': 'In Progress'},
            'assignee': {'id': 6},
            'priority': {'name': 'Medium'},
            'createdUser': {'id': 7},
            'milestone': [{'name': 'Milestone 2'}],
            'category': [{'id': 8}],
            'versions': [{'id': 9}],
            'startDate': '2023-10-11',
            'dueDate': '2023-10-16',
            'estimatedHours': 8.0,
            'actualHours': 6.0,
            'projectId': 116639,
            'issueKey': 'ABC-124',
            'updatedUser': {'id': 10},
            'updated': '2023-10-13T15:45:00Z',
            'id': 1002,
            'resolution': "Won't Fix",
            'parentIssueId': 1001,
            'created': '2023-10-11T11:45:00Z',
            'customFields': [],
            'releaseDueDate': '2023-10-25'
        }
    ]
    mock_requests_get.return_value = mock_response_issues
    # Mock database functions
    main.insert_issue = Mock()
    # Call the all_issues_in_a_project function
    project_id = 116639
    total_count = 2
    main.all_issues_in_a_project(cursor, total_count, project_id)


def test_project_exists():
    connection = main.create_db_connection()
    cursor = connection.cursor()
    project_id = 116639
    result = main.project_exists(cursor, project_id)
    assert result is True


def test_category_exists():
    cursor = Mock()
    backlog_category_id = 123
    cursor.fetchone.return_value = (1,)
    result = utils.category_exists(cursor, backlog_category_id)
    assert result is True


def test_check_for_updatepos():
    # Create a cursor object
    connection = main.create_db_connection()
    cursor = connection.cursor()
    # Create a user object
    user = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'backlog_user_id': '1234567890',
        'role_type': 1,
        'user_id': 1
    }

    # Insert the user into the database
    insert_query = ("INSERT INTO members (name, user_id,backlog_user_id, email,role_type, status, create_date, "
                    "update_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data = (user['name'], user['user_id'], user['backlog_user_id'], user['email'], user['role_type'], 1, create_date,
            update_date)
    cursor.execute(insert_query, data)
    # Check if the user exists in the database
    sql = "SELECT COUNT(*) FROM members WHERE name = %s AND email = %s AND backlog_user_id = %s AND role_type = %s"
    data = (user['name'], user['email'], user['backlog_user_id'], user['role_type'])
    cursor.execute(sql, data)
    count = cursor.fetchone()[0]
    # Assert that the user exists in the database
    assert count == 1
    # Update the user's information
    user['name'] = 'Jane Doe'
    user['email'] = 'jane.doe@example.com'
    user['backlog_user_id'] = '9876543210'
    user['role_type'] = 2
    # Call the check_for_update function
    result = utils.check_for_updation(cursor, user)
    # Assert that the function returns True
    assert result is True
    # Check if the user's information was updated in the database
    sql = "SELECT name, email, backlog_user_id, role_type FROM members WHERE user_id = %s"
    data = (user['user_id'],)
    cursor.execute(sql, data)
    cursor.fetchone()


@patch('main.create_db_connection')
def test_get_all_category_request_failure(mock_create_db_connection):
    mock_cursor = mock_create_db_connection.return_value.cursor()
    project_id = 123
    with patch(MAIN_REQUEST_GET, side_effect=requests.exceptions.RequestException("Test Error")):
        categories = main.get_all_category(mock_cursor, project_id)
        assert not categories


@pytest.fixture
def mock_cursor():
    cursor = Mock()
    return cursor


@pytest.fixture
def db_connection():
    connection = Mock()
    return connection


def test_project_existing_data_check_else_update_update(mock_cursor):
    project = {
        'name': 'New Project',
        'key': 'NEWPROJ',
        'id': 123
    }
    mock_cursor.fetchone.return_value = (0,)
    result = main.project_existing_data_check_else_update(mock_cursor, project)
    assert result is True


def test_project_existing_data_check_else_update_no_update(mock_cursor):
    project = {
        'name': 'Existing Project',
        'key': 'EXISTPROJ',
        'id': 456
    }
    # Mock the cursor's execute method to return a count of 1
    mock_cursor.fetchone.return_value = (1,)
    result = main.project_existing_data_check_else_update(mock_cursor, project)
    assert result is False


def test_check_for_project_member_update(mock_cursor, db_connection):
    member = {
        'project_id': 123,
        'member_id': 456,
        'member_role': 'New Role'
    }
    # Mock the get_project and get_member functions to return valid IDs
    mock_cursor.fetchone.return_value = (0,)
    result = main.check_for_project_member_updation(mock_cursor, member, db_connection)
    assert result is True


def test_check_for_project_member_updation_none_ids(mock_cursor, db_connection):
    member = {
        'project_id': 123,
        'member_id': 456,
        'member_role': 2
    }
    # Mock the get_project and get_member functions to return None
    mock_cursor.fetchone.return_value = (1,)
    result = main.check_for_project_member_updation(mock_cursor, member, db_connection)
    assert result is False


def test_check_for_updation_else_condition(mock_cursor):
    user = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'backlog_user_id': 123,
        'role_type': 'Developer',
        'user_id': 456
    }
    # Mock the cursor.execute and cursor.fetchone to return a non-zero count (e.g., 1)
    mock_cursor.fetchone.return_value = (1,)
    result = main.check_for_updation(mock_cursor, user)
    assert result is False


def test_get_project_else_condition(mock_cursor):
    project_id = 123  # Replace with the project_id you want to test
    mock_cursor.fetchone.return_value = None
    result = main.get_project(mock_cursor, project_id)
    assert result is None


def test_user_exists_in_members_count_greater_than_zero(mock_cursor):
    user_id = 123
    mock_cursor.fetchone.return_value = (1,)
    result = main.user_exists_in_members(mock_cursor, user_id, email=None)
    assert result is True


def test_insert_project_member(mock_cursor):
    project_member = {
        'member_role': 'Role 1',
    }
    member_id = 123
    project_id = 456
    created_date2 = '2023-01-01'
    updated_date2 = '2023-01-02'
    # Mock the cursor.execute method to capture the query and data
    captured_queries = []

    def execute(query, data):
        captured_queries.append((query, data))

    mock_cursor.execute = execute
    main.insert_project_member(mock_cursor, project_member, member_id, project_id, created_date2, updated_date2)
    expected_query = ("INSERT INTO projects_members (member_id, member_role, project_id, status, create_date, "
                      "update_date) VALUES (%s, %s, %s, %s, %s, %s)")
    expected_data = (member_id, project_member['member_role'], project_id, 1, created_date2, updated_date2)
    assert len(captured_queries) == 1
    assert captured_queries[0] == (expected_query, expected_data)


#
def test_insert_category_with_existing_project_id(mock_cursor):
    project_categories = {
        'projectId': 123,
        'id': 456,
        'name': 'Category Name'
    }
    create_date4 = '2023-10-09'
    update_date4 = '2023-10-09'
    mock_cursor.fetchone.return_value = (1,)
    result = utils.insert_category(mock_cursor, project_categories, create_date4, update_date4)
    # Ensure that the function returns None when an existing project ID is found
    assert result is None


@patch('main.get_project', return_value=None)
@patch('main.create_db_connection')
def test_insert_category_with_missing_project_id(mock_create_db_connection, mock_get_project):
    mock_cursor = mock_create_db_connection.return_value.cursor()
    project_categories = {
        'projectId': 123,
        'id': 456,
        'name': 'Category Name'
    }
    create5_date = '2023-10-09'
    update5_date = '2023-10-09'
    result = utils.insert_category(mock_cursor, project_categories, create5_date, update5_date)
    # Ensure that the function returns None when the project ID is not found
    assert result is None


@patch('main.create_db_connection')
def test_get_all_versions_request_failure(mock_create_db_connection):
    mock_cursor = mock_create_db_connection.return_value.cursor()
    project_id = 123
    with patch(MAIN_REQUEST_GET, side_effect=requests.exceptions.RequestException("Test Error")):
        versions = main.get_all_versions(mock_cursor, project_id)
        assert not versions
        assert Mock(Exception("Exception"))


@patch('main.create_db_connection')
@patch('main.check_backlog_api')
@patch(MAIN_REQUEST_GET,
       return_value=Mock(status_code=200, json=Mock(side_effect=ValueError("Test JSON Parse Error"))))
def test_get_all_versions_json_parse_failure(mock_create_db_connection, mock_check_backlog_api, mock_requests_get):
    mock_cursor = mock_create_db_connection.return_value.cursor()
    project_id = 123
    # Ensure that the check_backlog_api function returns None to simulate the BACKLOG_API_KEY not being set
    mock_check_backlog_api.return_value = None
    versions = main.get_all_versions(mock_cursor, project_id)
    # Assertions to check the expected behavior
    assert not versions
    mock_check_backlog_api.assert_called_once()


@patch('main.create_db_connection')
@patch('main.check_backlog_api')
@patch(MAIN_REQUEST_GET,
       return_value=Mock(status_code=200, json=lambda: [{"id": 1, "name": "Version 1", "startDate": "2023-01-01"}]))
def test_get_all_versions_duplicate_entry(mock_create_db_connection, mock_check_backlog_api, mock_requests_get):
    mock_cursor = mock_create_db_connection.return_value.cursor()
    project_id = 123
    mock_check_backlog_api.return_value = "your_api_key_here"
    # Assume that a duplicate entry is found in the database
    mock_cursor.fetchone.return_value = (123,)
    versions = main.get_all_versions(mock_cursor, project_id)
    # Assertions
    expected_versions = [
        {"description": None, "backlog_version_id": 1, "name": "Version 1", "project_id": None,
         "release_due_date": None,
         "start_date": "2023-01-01"}]
    assert versions == expected_versions
    mock_check_backlog_api.assert_called_once()


def test_check_backlog_api_without_api_key():
    main.BACKLOG_API_KEY = None
    result = main.check_backlog_api()
    assert result == []


def test_check_empty_response():
    response = []
    message = "Test Message"
    result = main.check_empty_response(response, message)
    assert result is None


def test_log_project_data():
    project = {
        'name': "name",
        'id': 1,
        'key': "key"
    }
    result = main.log_project_data(project)
    assert result is None


def test_project_version_exists_version_found():
    # Create a mock cursor
    mock_cursor = Mock()
    # Configure the cursor to return a result when execute is called
    mock_cursor.fetchone.return_value = (42,)
    # Call the function with a backlog_version_id
    version_id = utils.project_version_exists(mock_cursor, 1)
    # Check if the function returned the correct version_id
    assert version_id == 42


def test_project_version_exists_version_not_found():
    # Create a mock cursor
    mock_cursor = Mock()
    # Configure the cursor to return None when execute is called
    mock_cursor.fetchone.return_value = None
    # Call the function with a backlog_version_id
    version_id = utils.project_version_exists(mock_cursor, 1)
    # Check if the function returned None
    assert version_id is None


def test_check_batch_execution():
    # Create a mock database connection and cursor
    db = Mock()
    cursor = db.cursor()
    # Create a mock logger
    logger = Mock()
    # Case where count[0] is greater than 0
    cursor.fetchone.return_value = (1,)
    main.check_batch_execution(db, cursor, logger)
    # Case where count[0] is not greater than 0
    cursor.fetchone.return_value = (0,)
    main.check_batch_execution(db, cursor, logger)


def test_issue_exists():
    # Create a mock cursor
    cursor = Mock()
    # Test case 1: When the result is not None
    cursor.fetchone.return_value = (1,)  # Simulate a result
    issue = {"backlog_issue_id": 123, "project_id": 456}
    result = utils.issue_exists(cursor, issue)
    assert result == 1
    # Test case 2: When the result is None
    cursor.fetchone.return_value = None
    result = utils.issue_exists(cursor, issue)
    assert result is None


def test_get_category():
    # Create a mock cursor
    cursor = Mock()
    # Test case 1: When the result is not None
    cursor.fetchone.return_value = (1,)
    backlog_category_id = 123
    result = utils.get_category(cursor, backlog_category_id)
    assert result == 1  # En
    # Test case 2: When the result is None
    cursor.fetchone.return_value = None
    result = utils.get_category(cursor, backlog_category_id)
    assert result is None  # Ensure that the function returns None


def test_fetch_version():
    # Create a mock cursor
    cursor = Mock()
    # Test case 1: When the result is not None
    cursor.fetchone.return_value = (1,)
    backlog_version_id = 456
    result = utils.fetch_version(cursor, backlog_version_id)
    assert result == 1
    # Test case 2: When the result is None
    cursor.fetchone.return_value = None
    result = utils.fetch_version(cursor, backlog_version_id)
    assert result is None


def test_get_member_exists(mock_cursor):
    member_id = 123
    # Mock the cursor.execute to return a result (matching condition)
    mock_cursor.fetchone.return_value = (1,)
    result = main.get_member(mock_cursor, member_id)
    assert result == 1


def test_get_member_with_existing_member(cov):
    # Mock the cursor object to return a result.
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = (1,)
    # Call the `get_member()` function with a valid backlog user ID.
    member_id = utils.get_member(mock_cursor, 12345)
    # Assert that the `get_member()` function returned the correct member ID.
    assert member_id == 1
    # Assert that the `cursor.execute()` method was called with the correct SQL statement and parameters.
    mock_cursor.execute.assert_called_once_with("SELECT id FROM members WHERE user_id = %s", (12345,))
    # Assert that the `cursor.fetchone()` method was called once.
    mock_cursor.fetchone.assert_called_once()


def test_insert_issue():
    date1 = "2023-10-12T16:00:00Z"
    date2 = "2023-10-12 16:26:34.976633"
    # Create a mock cursor
    cursor = Mock()
    # Test data
    issue = {
        "project_id": 1,
        "category": ["Category1"],
        "issue_type": "Bug",
        "subject": "Sample Issue",
        "description": "This is a sample issue description.",
        "issue_status": "Open",
        "priority": "High",
        "estimated_hours": 5.0,
        "actual_hours": 2.5,
        "issue_key": "ISSUE-123",
        "created_in_backlog": date1,
        "updated_in_backlog": date1,
        "backlog_issue_id": 456,
        "issue_start_date": date1,
        "issue_due_date": date1,
        "milestone": "Milestone1",
        "assignee_id": 789,
        "registered_user_id": 101,
        "updated_user": 102,
        "create_date": date2,
        "update_date": date2,
        "versions": 123,
        "status": 1,
        "resolution": "fixed"
    }
    # Mock the results of get_project, get_category, get_version, and other functions
    with patch("utils.get_project") as mock_get_project, \
            patch("utils.get_category") as mock_get_category, \
            patch("utils.fetch_version") as mock_fetch_version, \
            patch("utils.fetch_member_id") as mock_fetch_member_id:
        # Mock the results of the functions to return expected values
        mock_get_project.return_value = 42
        mock_get_category.return_value = 123
        mock_fetch_version.return_value = 567
        mock_fetch_member_id.return_value = 789
        # Configure the execute method of the cursor to return a custom Mock
        execute_mock = Mock()
        cursor.execute.return_value = execute_mock
        # Configure the fetchone method of the executes Mock
        execute_mock.fetchone.return_value = (42,)
        # Mock current_datetime (replace with the actual value if needed)
        with patch("utils.current_datetime", date2):
            # Call the function
            utils.insert_issue(cursor, issue)


def test_issue_category_mapping_with_result():
    # Prepare a mock cursor
    mock_cursor = Mock()
    # Define a sample issue with a backlog_issue_id
    issue = {
        "backlog_issue_id": 123,
        "category": [1, 2, 3]
    }
    # Mock the cursor.execute method and fetchone method to return a result
    mock_cursor.fetchone.return_value = (42,)
    utils.get_category.side_effect = [100, 200, 300]
    # Call the function
    utils.issue_category_mapping(mock_cursor, issue)


@patch(MAIN_REQUEST_GET)
@patch('main.create_db_connection')
def test_get_all_project_members(
        mock_create_db_connection,
        mock_requests_get
):
    # Prepare mock response from requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "userId": "user1",
            "name": "User 1",
            "roleType": 1,
            "mailAddress": "user1@example.com"
        },
        {
            "id": 2,
            "userId": "user2",
            "name": "User 2",
            "roleType": 2,
            "mailAddress": "user2@example.com"
        }
    ]
    mock_requests_get.return_value = mock_response
    # Mock the database cursor and connection
    mock_cursor = Mock()
    mock_db = Mock()
    mock_create_db_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)
    # case 1 : Mock the behavior of main.get_all_project_members to return a non-None value
    main.get_all_project_members.return_value = [
        {
            "member_id": 12345,
            "member_role": 1,
            "project_id": 116639,
            "status": 1,
            "create_date": "2023-10-10 15:57:22.872624",
            "update_date": "2023-10-10 15:57:22.872624"
        }
    ]
    # Replace with your test data and assertions for get_all_project_members
    project_id = 116639
    result = main.get_all_project_members(cursor=mock_cursor, project_id=project_id, db=mock_db)
    assert result is not None
    mock_requests_get.assert_called_once()
    #  case 2 : make user_exists_in_project return none
    main.get_all_project_members.return_value = None
    main.get_all_project_members(cursor=mock_cursor, project_id=project_id, db=mock_db)


@pytest.mark.xfail(reason="Expected to raise an exception")
def test_create_db_connection_with_invalid_credentials():
    # Mock the environment variables to simulate invalid database credentials.
    with patch.dict("os.environ",
                    {"DBHOST": "invalid_host", "USER_NAME": "invalid_user", "PASSWORD": "invalid_password",
                     "DATABASE": "invalid_database", "PORT": "invalid_port"}):
        # Call the `create_db_connection()` function.
        connection = config.create_db_connection()
        # Assert that the `create_db_connection()` function raised an exception.
        assert connection is None


def test_get_all_backlog_projects():
    # Create mock objects and configure their behavior
    connection = main.create_db_connection()
    cursor = Mock()

    # Mock the requests.get method
    with patch(MAIN_REQUEST_GET) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "name": "Project 1",
                "id": 123,
                "projectKey": "PROJ1"
            },
            {
                "name": "Project 2",
                "id": 456,
                "projectKey": "PROJ2"
            }
        ]
        mock_get.return_value = mock_response

        # Mock other functions as needed
        with patch.object(main, 'project_exists', return_value=False):
            with patch.object(main, 'insert_project'):
                with patch.object(main, 'log_project_data'):
                    with patch.object(main, 'get_all_project_users'):
                        with patch.object(main, 'get_all_project_members'):
                            with patch.object(main, 'get_all_category'):
                                with patch.object(main, 'get_all_versions'):
                                    with patch.object(main, 'get_all_issue_count', return_value=10):
                                        with patch.object(main, 'all_issues_in_a_project'):
                                            # Call the function to be tested
                                            main.get_all_backlog_projects(cursor, connection)


def test_existing_project_with_updates():
    cursor = Mock()
    db = main.create_db_connection()

    # Mock the requests.get method
    with patch(MAIN_REQUEST_GET) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "name": "Project 1",
                "id": 123,
                "projectKey": "PROJ1"
            }
        ]
        mock_get.return_value = mock_response

        with patch.object(main, 'save_daily_bug_data', return_value=True):
            # Mock the project_exists function to simulate an existing project
            with patch.object(main, 'project_exists', return_value=True):
                # Mock other functions as needed
                with patch.object(main, 'project_existing_data_check_else_update', return_value=True):
                    with patch.object(main, 'get_all_project_users'):
                        with patch.object(main, 'get_all_project_members'):
                            with patch.object(main, 'get_all_category'):
                                with patch.object(main, 'get_all_versions'):
                                    with patch.object(main, 'get_all_issue_count', return_value=10):
                                        with patch.object(main, 'all_issues_in_a_project'):
                                            main.get_all_backlog_projects(cursor, db)


@pytest.fixture
def mock_cursor():
    return MagicMock()


@pytest.fixture
def mock_logger():
    return MagicMock()


def test_save_daily_bug_data_insert(mock_cursor, mock_logger):
    project_id = 1
    mock_cursor.execute.return_value = None
    utils.save_daily_bug_data(project_id, mock_logger, mock_cursor)
    print(mock_cursor.execute.call_count, mock_logger.info.call_count)
    assert mock_cursor.execute.call_count == 7
    assert mock_logger.info.call_count == 6


def test_save_daily_bug_data_update(mock_cursor, mock_logger):
    project_id = 1
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.execute.return_value = None
    utils.save_daily_bug_data(project_id, mock_logger, mock_cursor)


if __name__ == '__main__':
    pytest.main(['-v', '--cov=main', '--cov=util', '--cov=config', 'tests.py'])
