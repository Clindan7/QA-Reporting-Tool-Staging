from dotenv import load_dotenv
from config import create_db_connection, BACKLOG_API_KEY, BACKLOG_BASE_URL
from utils import project_version_exists, insert_version, category_exists, insert_category, user_exists_in_members, \
    insert_user, check_for_updation, user_exists_in_project, get_member, get_project, insert_project_member, \
    check_for_project_member_updation, insert_issue, issue_category_mapping, project_exists, \
    insert_project, project_existing_data_check_else_update, check_batch_execution, update_batch_info, \
    save_daily_bug_data
import datetime
import requests
import logging

load_dotenv()

# logger config
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Get the current date and time
current_datetime = datetime.datetime.now()
create_date = current_datetime
update_date = current_datetime


def check_empty_response(response, message):
    if len(response) == 0:
        logger.info(f" {message} Response is empty (status 200, empty list).")


def check_backlog_api():
    if not BACKLOG_API_KEY:
        logger.error("BACKLOG_API_KEY is not set")
        return []


# get all versions list from backlog and save it itn db
def get_all_versions(cursor, project_id):
    logger.info("get_all_versions EXECUTION STARTED")
    check_backlog_api()
    url = f'{BACKLOG_BASE_URL}api/v2/projects/{project_id}/versions'
    params = {"apiKey": BACKLOG_API_KEY}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            versions = response.json()
            check_empty_response(versions, "version")
            project_versions = [
                {
                    'backlog_version_id': version["id"],
                    'project_id': version.get("projectId"),
                    'description': version.get("description"),
                    'start_date': version["startDate"],
                    'name': version.get("name"),
                    'release_due_date': version.get("releaseDueDate")
                }
                for version in versions
            ]
            for version in project_versions:
                version_id = project_version_exists(cursor, version['backlog_version_id'])
                if not version_id:
                    insert_version(cursor, version, create_date, update_date)
                    log_message = f"inserted version details are -->  \n" \
                                  f"backlog_version_id: {version['backlog_version_id']}\n" \
                                  f"project_id: {version['project_id']}\n" \
                                  f"description: {version['description']}\n" \
                                  f"start_date: {version['start_date']}\n" \
                                  f"release_due_date: {version['release_due_date']}\n" \
                                  f"name: {version['name']}\n"
                    logger.info(log_message)
                else:
                    logger.info(f"duplicate entry for version --> {version}. ")
            return project_versions
    except requests.exceptions.RequestException as e:
        logger.error("Request failed : %s", str(e))
    except ValueError as e:
        logger.error("Failed to parse JSON response = %s", str(e))

    return []


# to get all category list from backlog and store it into db
def get_all_category(cursor, project_id):
    logger.info("get_all_category EXECUTION STARTED")
    check_backlog_api()
    url = f'{BACKLOG_BASE_URL}api/v2/projects/{project_id}/categories'
    params = {"apiKey": BACKLOG_API_KEY}
    try:
        logger.info("getting all categories under project : started\n")
        response = requests.get(url, params=params)
        if response.status_code == 200:
            categories = response.json()
            project_categories = [
                {
                    'id': category["id"],
                    'projectId': category.get("projectId"),
                    'name': category.get("name")
                }
                for category in categories
            ]
            for category in project_categories:
                if not category_exists(cursor, category['id']):
                    insert_category(cursor, category, create_date, update_date)
                    log_message = f"inserted category -->  \n" \
                                  f"Category ID: {category['id']}\n" \
                                  f"Category Name: {category['name']}\n" \
                                  f"Project ID: {category['projectId']}\n"
                    logger.info(log_message)
                else:
                    logger.info(f"duplicate entry for category --> {category}. ")
            return project_categories
    except requests.exceptions.RequestException as e:
        logger.error("Request  failed: %s", str(e))
    return []


# to get all users in backlog and add to
def get_all_project_users(cursor, project_id):
    logger.info("get_all_users EXECUTION STARTED")
    check_backlog_api()
    url = f'{BACKLOG_BASE_URL}api/v2/projects/{project_id}/users'
    params = {"apiKey": BACKLOG_API_KEY}
    try:
        logger.info("getting backlog space users started \n")
        response = requests.get(url, params=params)
        users = response.json()
        user_details = [
            {
                'user_id': user["id"],
                'backlog_user_id': user.get("userId"),
                'name': user.get("name", "none"),
                'role_type': user.get("roleType"),
                'email': user.get("mailAddress")
            }
            for user in users
        ]
        for user in user_details:
            user_exists = user_exists_in_members(cursor, user['user_id'], user['email'])
            if not user_exists:
                insert_user(cursor, user, create_date, update_date)
                log_message = "inserted user details \n" \
                              f"User ID: {user['user_id']}\n" \
                              f"User Name: {user['name']}\n" \
                              f"User User ID: {user['backlog_user_id']}\n" \
                              f"User Role Type: {user['role_type']}\n" \
                              f"User Mail Address: {user['email']}"
                logger.info(log_message)
            logger.warning(f"duplicate entry for user --> {user}. ")
            updated_member_data = check_for_updation(cursor, user)
            if updated_member_data:
                logger.info(f"updated the member data having id :{user['user_id']}. Updated details are : {user}")
        return user_details
    except requests.exceptions.RequestException as e:
        logger.error(" Request failed: %s", str(e))
    return []


# function get project member-list and maps member table with project table
def get_all_project_members(cursor, project_id, db):
    logger.info("get_all_project_members EXECUTION STARTED")
    check_backlog_api()
    url = f'{BACKLOG_BASE_URL}api/v2/projects/{project_id}/users'
    params = {"apiKey": BACKLOG_API_KEY}
    try:
        logger.info("GETTING PROJECT MEMBERS FROM BACKLOG \n")
        response = requests.get(url, params=params)
        response.raise_for_status()
        all_project_members = response.json()
        project_members = [
            {
                'member_id': project_member["id"],
                'member_role': project_member["roleType"],
                'project_id': project_id
            }
            for project_member in all_project_members
        ]
        for member in project_members:
            if not user_exists_in_project(cursor, member['member_id'], member['project_id']):
                member_id = get_member(cursor, member['member_id'])
                project_id = get_project(cursor, member['project_id'])
                insert_project_member(cursor, member, member_id, project_id, create_date, update_date)
                log_message = "inserted project member details are \n" \
                              f"PROJECT ID: {project_id}\n" \
                              f"MEMBER ID: {member_id}\n" \
                              f"MEMBER ROLE: {member['member_role']}\n"
                logger.info(log_message)
            logger.info(f" --> Duplicate entry for project_members having details of {member}")
            updated_project_member_data = check_for_project_member_updation(cursor, member, db)
            if updated_project_member_data:
                logger.info(f" Updated project member details are : {member}")


    except requests.exceptions.RequestException as e:
        logger.error(str(e))
    return []


# get all issue count from backlog and save it itn db
def get_all_issue_count(project_id):
    logger.info("get_all_issues EXECUTION STARTED")
    check_backlog_api()

    url1 = f'{BACKLOG_BASE_URL}api/v2/issues/count'
    params = {
        "apiKey": BACKLOG_API_KEY,
        "projectId[]": project_id,
    }
    try:
        count = requests.get(url1, params=params).json()
        total_count = count['count']
        logger.info(f"total issues in project having id{project_id} is {total_count}")
        logger.info("Updating total bug count in db")
        print("all issues count --> ", total_count)
        logger.info(f"all issues count --> {total_count}")
        return total_count
    except requests.exceptions.RequestException as e:
        logger.error(e)


def all_issues_in_a_project(cursor, total_count, project_id):
    logger.info("getting all the issues under the project")
    url = f'{BACKLOG_BASE_URL}api/v2/issues'
    try:
        items_per_page = 100  # max no. of items from a page is 100
        offset = 0
        project_issues = []  # Initialize an empty list to store all issues
        while offset < total_count:
            # Calculate the count for this page
            page_count = min(items_per_page, total_count - offset)
            # Get total issues in the current page
            params = {
                "apiKey": BACKLOG_API_KEY,
                "projectId[]": project_id,
                "offset": offset,
                "count": page_count,
            }
            logger.info(
                f"getting issues of the project from backlog. params [offset= {offset}, page_count= {page_count}]")
            response = requests.get(url, params=params)
            if response.status_code == 200:
                issues = response.json()
                if issues is not None:
                    all_project_issues = issue_list(issues, project_issues)
                else:
                    logger.warning("Received empty JSON response from the API.")
                offset += page_count
            else:
                logger.warning("Failed to retrieve issues. Status code: %d", response.status_code)
                break
        logger.info(f"length of all issue list for a single prjt: {len(all_project_issues)}")
        print("length of all issue list for a single prjt)", len(all_project_issues))
        logger.info(f"all project issue list){all_project_issues}")

        for issue in all_project_issues:
            logger.info("insert all issues under the project getting started")
            insert_issue(cursor, issue)
            logger.info("issue category mapping")
            issue_category_mapping(cursor, issue)
            logger.info(f"All issues under the projectId having  backlog issue id {issue['backlog_issue_id']} and "
                        f"project id {issue['project_id']}, has been successfully inserted")

    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", str(e))
    return all_project_issues


def extract_value(issue, key, default="None"):
    keys = key.split(".")
    value = issue
    try:
        for k in keys:
            value = value[k]

        return value if value is not None else default
    except (KeyError, TypeError):
        return default


def issue_list(issues, all_project_issues):
    for issue in issues:
        issue_data = {
            'issue_type': extract_value(issue, "issueType.name"),
            'subject': extract_value(issue, "summary"),
            'description': extract_value(issue, "description"),
            'issue_status': extract_value(issue, "status.name"),
            'assignee_id': extract_value(issue, "assignee.id", None),
            'priority': extract_value(issue, "priority.name"),
            'registered_user_id': extract_value(issue, "createdUser.id", None),
            'milestone': issue["milestone"][0]["name"] if isinstance(issue.get("milestone"), list) and
                                                          issue["milestone"] else "None",
            'category': [cat["id"] for cat in issue["category"]] if isinstance(issue.get("category"),
                                                                               list) else "None",
            'versions': [ver["id"] for ver in issue["versions"]] if isinstance(issue.get("versions"),
                                                                               list) else "None",
            'issue_start_date': issue.get("startDate"),
            'issue_due_date': issue.get("dueDate"),
            'estimated_hours': issue.get("estimatedHours"),
            'actual_hours': issue.get("actualHours"),
            'project_id': extract_value(issue, "projectId"),
            'issue_key': extract_value(issue, "issueKey"),
            'updated_user': extract_value(issue, "updatedUser.id", None),
            'created_in_backlog': extract_value(issue, "created"),
            'updated_in_backlog': extract_value(issue, "updated"),
            'backlog_issue_id': extract_value(issue, "id"),
            'resolution': extract_value(issue, "resolution.name"),
            'parentIssueId': extract_value(issue, "parentIssueId"),
            'created': extract_value(issue, "created"),
            'customFields': extract_value(issue, "customFields", []),
            'release_due_date': extract_value(issue, "releaseDueDate"),
        }

        all_project_issues.append(issue_data)

    return all_project_issues


# getting all project list from backlog api and stores in db
def get_all_backlog_projects(cursor, db):
    logger.info("get_all_backlog_projects STARTED EXECUTION : ")
    check_backlog_api()

    url = f'{BACKLOG_BASE_URL}api/v2/projects'
    params = {"apiKey": BACKLOG_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        projects = response.json()

        project_details = [
            {
                'name': project["name"],
                'id': project["id"],
                'key': project["projectKey"]
            }
            for project in projects
        ]
        for project in project_details:
            if not project_exists(cursor, project['id']):
                insert_project(cursor, project, create_date, update_date)
                log_project_data(project)
                get_all_project_users(cursor, project["id"])
                # function for set mapping project with members
                get_all_project_members(cursor, project['id'], db)
                # function for getting all categories under the project
                get_all_category(cursor, project['id'])
                # function for getting all versions under the project
                get_all_versions(cursor, project['id'])
                # function for getting all issues count under the project
                total_issue_count = get_all_issue_count( project['id'])
                # function for getting all issues under the project
                all_issues_in_a_project(cursor, total_issue_count, project['id'])
            else:

                logger.warning(f"duplicate entry for Project --> {project}. ")
                logger.info(f"checking for any updates in existing project data --> {project}. ")
                updated_project_data = project_existing_data_check_else_update(cursor, project)
                if updated_project_data:
                    logger.info(f"updated the project data having id :{project['id']}. Updated details are : {project}")
                else:
                    logger.info("no updates found.")
                get_all_project_users(cursor, project["id"])
                get_all_project_members(cursor, project['id'], db)
                get_all_category(cursor, project['id'])
                get_all_versions(cursor, project['id'])
                total_issue_count = get_all_issue_count( project['id'])
                all_issues_in_a_project(cursor, total_issue_count, project['id'])
                save_daily_bug_data(project['id'], logger, cursor)


    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", str(e))
    return []


def log_project_data(project):
    log_message = "inserted project details are : \n" \
                  f"Project Name: {project.get('name', 'N/A')}\n" \
                  f"Project ID: {project.get('id', 'N/A')}\n" \
                  f"Project Key: {project.get('key', 'N/A')}"
    logger.info(log_message)


if __name__ == '__main__':

    try:
        db = create_db_connection()
        cursor = db.cursor()
        if check_batch_execution(db, cursor, logger):
            get_all_backlog_projects(cursor, db)
            update_batch_info(db, cursor, 1, logger)
            db.commit()
        cursor.close()
        db.close()
        print("Database connection closed successfully.")
        logger.info("database connection closed successfully")

    except Exception as e:
        logger.warning(e)
