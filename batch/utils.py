import datetime

current_datetime = datetime.datetime.now()
update_date = create_date = current_datetime


def project_exists(cursor, project_id):
    sql = "SELECT COUNT(*) FROM projects WHERE backlog_project_id = %s"
    cursor.execute(sql, (project_id,))
    count = cursor.fetchone()[0]
    return count > 0


def check_for_updation(cursor, user):
    sql = "SELECT COUNT(*) FROM members WHERE name = %s AND email = %s AND backlog_user_id = %s AND role_type = %s"
    data = (user['name'], user['email'], user['backlog_user_id'], user['role_type'])
    cursor.execute(sql, data)
    count = cursor.fetchone()[0]
    if count == 0:
        update_query = "UPDATE members SET name = %s, email = %s,  backlog_user_id = %s, role_type = %s, update_date = %s WHERE user_id = %s"
        update_data = (
            user['name'], user['email'], user['backlog_user_id'], user['role_type'], update_date, user['user_id'])
        cursor.execute(update_query, update_data)
        return True
    else:
        return False


def check_for_project_member_updation(cursor, member, db):
    project_id = get_project(cursor, member['project_id'])
    member_id = get_member(cursor, member['member_id'])

    sql = "SELECT COUNT(*) FROM projects_members WHERE member_role = %s AND member_id= %s AND project_id =%s"
    data = (member['member_role'], member_id, project_id)
    cursor.execute(sql, data)
    count = cursor.fetchone()[0]
    if count == 0:
        update_query = "UPDATE projects_members SET member_role = %s WHERE member_id = %s AND project_id = %s"
        update_data = (member['member_role'], member_id, project_id)
        cursor.execute(update_query, update_data)
        db.commit()
        return True
    else:
        return False


def project_existing_data_check_else_update(cursor, project):
    sql = "SELECT COUNT(*) FROM projects WHERE name = %s AND project_code = %s AND backlog_project_id = %s"
    data = (project['name'], project['key'], project['id'])
    cursor.execute(sql, data)
    count = cursor.fetchone()[0]
    if count == 0:
        update_query = ("UPDATE projects SET name = %s, project_code = %s, update_date = %s WHERE backlog_project_id = "
                        "%s")
        update_data = (project['name'], project['key'], update_date, project['id'])
        cursor.execute(update_query, update_data)
        return True
    else:
        return False


def insert_project(cursor, project, create_date, update_date):
    insert_query = ("INSERT INTO projects (name, backlog_project_id, project_code, status, create_date, update_date, "
                    "release_date, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data = (project['name'], project['id'], project['key'], 1, create_date, update_date, create_date, "None")
    cursor.execute(insert_query, data)
    cursor.execute('SELECT LAST_INSERT_ID()')
    cursor.fetchone()[0]


def get_project(cursor, project_id):
    sql = "SELECT id FROM projects WHERE backlog_project_id = %s"
    cursor.execute(sql, (project_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def user_exists_in_members(cursor, user_id, email):
    sql = "SELECT COUNT(*) FROM members WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    count = cursor.fetchone()[0]
    if count > 0:
        return True
    else:
        if email is not None:
            sql1 = "SELECT * FROM members WHERE email like %s and user_id= %s"
            cursor.execute(sql1, (email, user_id))
            res = cursor.fetchone()
            if res and res['email'] == email:
                return True
            else:
                return False
        else:
            return False


def insert_user(cursor, user, create_date, update_date):
    insert_query = ("INSERT INTO members (name, user_id,backlog_user_id, email,role_type, status, create_date, "
                    "update_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data = (user['name'], user['user_id'], user['backlog_user_id'], user['email'], user['role_type'], 1, create_date,
            update_date)
    cursor.execute(insert_query, data)


def user_exists_in_project(cursor, member_id, project_id):
    project = get_project(cursor, project_id)
    sql = """
        SELECT COUNT(*) FROM members AS m
        INNER JOIN projects_members AS pm ON m.id = pm.member_id
        WHERE m.user_id = %s AND pm.project_id=%s
        """
    cursor.execute(sql, (member_id, project))
    count = cursor.fetchone()[0]
    return count > 0


def insert_project_member(cursor, project_member, member_id, project_id, create_date, update_date):
    insert_query = ("INSERT INTO projects_members (member_id, member_role, project_id, status, create_date, "
                    "update_date) VALUES (%s, %s, %s, %s, %s, %s)")
    data = (member_id, project_member['member_role'], project_id, 1, create_date, update_date)
    cursor.execute(insert_query, data)


def category_exists(cursor, backlog_category_id):
    sql = "SELECT COUNT(*) FROM categories WHERE backlog_category_id = %s"
    cursor.execute(sql, (backlog_category_id,))
    count = cursor.fetchone()[0]
    return count > 0


def insert_category(cursor, project_categories, create_date, update_date):
    project_id = get_project(cursor, project_categories['projectId'])
    insert_query = ("INSERT INTO categories ( project_id,backlog_category_id, name, status, create_date, update_date) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")
    data = (project_id, project_categories['id'], project_categories['name'], 1, create_date, update_date)
    cursor.execute(insert_query, data)


def project_version_exists(cursor, backlog_version_id):
    sql = "SELECT id FROM versions WHERE backlog_version_id = %s"
    cursor.execute(sql, (backlog_version_id,))
    result = cursor.fetchone()
    if result is not None:
        version_id = result[0]
        return version_id
    else:
        return None


def insert_version(cursor, version, create_date, update_date):
    project_id = get_project(cursor, version['project_id'])

    insert_query = ("INSERT INTO versions ( project_id, backlog_version_id, name, description, start_date, "
                    "release_due_date, create_date, update_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data = (project_id, version['backlog_version_id'], version['name'], version['description'], version['start_date'],
            version['release_due_date'], create_date, update_date, 1)
    cursor.execute(insert_query, data)


def check_batch_execution(db, cursor, logger):
    global sub_batch_id
    logger.info(' \n checking if the same batch is in execution')
    cursor.execute('SELECT count(*) FROM sub_batch_process WHERE status=0 and batch_process_id=1')
    count = cursor.fetchone()
    if count[0] > 0:
        cursor.close()
        db.close()
        logger.info(
            "\n \n*************  The batch was terminated because there was a running batch present at {}*************"
            .format(current_datetime))
        return False
    else:
        logger.info('No instances of QA Report generation batch is in execution. Batch execution can be carried out')

        query = ("INSERT INTO sub_batch_process(batch_process_id, status, start_time,create_date,update_date) VALUES"
                 " (%s, %s, %s, %s, %s)")
        data = (1, 0, current_datetime, current_datetime, current_datetime)
        cursor.execute(query, data)
        logger.info("inserted entry to batch_process_table keeping status as 0 ")
        cursor.execute('SELECT LAST_INSERT_ID()')
        sub_batch_id = cursor.fetchone()[0]
        db.commit()
        logger.info(
            " \n \n ****************************batch execution started  at {} ***************************** \n\n "
            .format(current_datetime))
        return True


def update_batch_info(db, cursor, status, logger):
    global sub_batch_id
    end_time = datetime.datetime.now()

    if status == 1:
        query = "UPDATE sub_batch_process SET status=%s, end_time=%s,update_date=%s WHERE id=%s"
        data = (status, end_time, update_date, sub_batch_id)
        cursor.execute(query, data)
    else:
        query = "UPDATE sub_batch_process SET status=%s, end_time=%s,update_date=%s, WHERE id=%s"
        data = (2, end_time, update_date, sub_batch_id)
        cursor.execute(query, data)
    db.commit()
    logger.info('updated batch_info table with id {} and batch_id 1'.format(sub_batch_id))
    logger.info(
        "\n \n************batch execution successfully completed at {}***********\n\n".format(
            current_datetime))


def issue_exists(cursor, issue):
    project_id = get_project(cursor, issue["project_id"])
    sql = "SELECT id FROM project_issues WHERE backlog_issue_id = %s and project_id=%s"
    cursor.execute(sql, (issue["backlog_issue_id"], project_id))
    result = cursor.fetchone()
    if result is not None:
        issue_id = result[0]
        return issue_id
    else:
        return None


def get_category(cursor, backlog_category_id):
    if backlog_category_id is not None:
        sql = "SELECT id FROM categories WHERE backlog_category_id = %s"
        cursor.execute(sql, (backlog_category_id,))
        result = cursor.fetchone()

        if result:
            return result[0]
    return None


def fetch_version(cursor, backlog_version_id):
    if backlog_version_id:
        sql = "SELECT id FROM versions WHERE backlog_version_id = %s"
        cursor.execute(sql, (backlog_version_id,))
        result = cursor.fetchone()

        if result:
            return result[0]

    return None


def get_member(cursor, backlog_user_id):
    sql = "SELECT id FROM members WHERE user_id = %s"
    cursor.execute(sql, (backlog_user_id,))
    result = cursor.fetchone()[0]
    if result:
        return result
    else:
        return None


def fetch_member_id(cursor, member_id):
    if member_id:
        sql = "SELECT id FROM members WHERE user_id = %s"
        cursor.execute(sql, (member_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None


def insert_issue(cursor, issue):
    if isinstance(issue["versions"], list) and len(issue["versions"]) > 0:
        version_id = issue['versions'][0]
    else:
        version_id = None

    project_id = get_project(cursor, issue["project_id"])
    version_id = fetch_version(cursor, version_id)
    assignee_id = fetch_member_id(cursor, issue["assignee_id"])
    registered_user_id = fetch_member_id(cursor, issue["registered_user_id"])
    updated_user_id = fetch_member_id(cursor, issue["updated_user"])
    status = 1
    # Conversion to a Python datetime object
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    formatted_updated_in_backlog = datetime.datetime.strptime(issue['updated_in_backlog'], date_format) if \
        issue['updated_in_backlog'] is not None else None
    formatted_created_in_backlog = datetime.datetime.strptime(issue['created_in_backlog'], date_format) if \
        issue['created_in_backlog'] is not None else None
    formatted_issue_start_date = datetime.datetime.strptime(issue['issue_start_date'], date_format) if (
            issue['issue_start_date'] is not None) else None
    formatted_issue_due_date = datetime.datetime.strptime(issue["issue_due_date"], date_format) if (
            issue['issue_due_date'] is not None) else None

    sql = """
        INSERT INTO project_issues (
          issue_type,
          subject,
          description,
          issue_status,
          priority,
          issue_start_date,
          issue_due_date,
          estimated_hours,
          actual_hours,
          issue_key,
          updated_in_backlog,
          backlog_issue_id,
          create_date,
          update_date,
          assignee_id,
          milestone,
          project_id,
          registered_user_id,
          updated_user_id,
          `versions_id`,
          status,
          created_in_backlog,
          resolution
        ) VALUES (
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON DUPLICATE KEY UPDATE
          issue_type = VALUES(issue_type),
          subject = VALUES(subject),
          description = VALUES(description),
          issue_status = VALUES(issue_status),
          priority = VALUES(priority),
          issue_start_date = VALUES(issue_start_date),
          issue_due_date = VALUES(issue_due_date),
          estimated_hours = VALUES(estimated_hours),
          actual_hours = VALUES(actual_hours),
          issue_key = VALUES(issue_key),
          updated_in_backlog = VALUES(updated_in_backlog),
          backlog_issue_id = VALUES(backlog_issue_id),
          create_date = VALUES(create_date),
          update_date = VALUES(update_date),
          assignee_id = VALUES(assignee_id),
          milestone = VALUES(milestone),
          project_id = VALUES(project_id),
          registered_user_id = VALUES(registered_user_id),
          updated_user_id = VALUES(updated_user_id),
          `versions_id` = VALUES(versions_id),
          status=VALUES(status),
          created_in_backlog=VALUES(created_in_backlog),
          resolution=VALUES(resolution)
        """
    data = (
        issue['issue_type'],
        issue['subject'],
        issue['description'],
        issue['issue_status'],
        issue['priority'],
        formatted_issue_start_date,
        formatted_issue_due_date,
        issue['estimated_hours'],
        issue['actual_hours'],
        issue['issue_key'],
        formatted_updated_in_backlog,
        issue['backlog_issue_id'],
        create_date,
        update_date,
        assignee_id,
        issue['milestone'],
        project_id,
        registered_user_id,
        updated_user_id,
        version_id,
        status,
        formatted_created_in_backlog,
        issue['resolution'],
    )
    cursor.execute(sql, data)


def issue_category_mapping(cursor, issue):
    backlog_issue_id = issue['backlog_issue_id']
    sql = "SELECT id FROM project_issues WHERE backlog_issue_id=%s"
    cursor.execute(sql, (backlog_issue_id,))
    result = cursor.fetchone()

    if result:
        issue_id = result[0]
        categories = issue.get("category", [])

        for category_id in categories:
            # Process each category_id here
            category_id = get_category(cursor, category_id)
            sql1 = "SELECT COUNT(*) FROM projects_issues_categories WHERE project_issues_id=%s AND category_id=%s"
            cursor.execute(sql1, (issue_id, category_id,))
            count = cursor.fetchone()[0]

            if count == 0:
                # Only insert if the category is not already mapped
                sql = (
                    "INSERT INTO projects_issues_categories (project_issues_id, category_id, create_date, "
                    "update_date) VALUES (%s, %s, %s, %s)")
                data = (issue_id, category_id, create_date, update_date)
                cursor.execute(sql, data)


def save_daily_bug_data(project_id, logger, cursor):
    bug_count = None
    project_id = get_project(cursor, project_id)
    current_date = datetime.datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    test_case_choices = ['API', 'UI']

    for category in test_case_choices:
        logger.info(f"started bug summary saving for project id :{project_id} and issue category {category}")

        sql = ("SELECT COUNT(*) FROM project_issues AS pi "
               "INNER JOIN projects_issues_categories AS pic ON pi.id = pic.project_issues_id "
               "INNER JOIN categories AS pc ON pc.id = pic.category_id "
               "WHERE pi.project_id = %s AND pc.name LIKE %s AND "
               "pi.issue_type = 'Bug' AND pi.issue_status != 'closed'")

        data = (project_id, category)
        cursor.execute(sql, data)
        result = cursor.fetchone()

        if result:
            logger.info(f"Open bugs today until {current_datetime} is {result[0]} for the project"
                        f" having id : {project_id} having category {category}")
            bug_count = result[0]

        sql1 = "SELECT id FROM bug_summary where project_id=%s and test_case_choice =%s and date(create_date)=%s"
        cursor.execute(sql1, (project_id, category, formatted_date))
        bug_summary = cursor.fetchone()

        if bug_summary:
            logger.info(f" Updating Bug summary table having project id :{project_id} on date {current_datetime}.\n "
                        f"Open Bug count ={bug_count} having category {category} ")
            sql11 = ("UPDATE bug_summary SET open_bugs = %s, update_date = %s WHERE project_id = %s "
                     "AND date(create_date) = %s AND test_case_choice = %s")
            cursor.execute(sql11, (bug_count, current_datetime, project_id, current_date, category))

        else:
            logger.info(f" Inserting Bug summary table having project id :{project_id} on date {current_datetime}.\n "
                        f"Open Bug count ={bug_count} having category {category} ")
            sql2 = (
                "INSERT INTO bug_summary (open_bugs, project_id, status, create_date, update_date, test_case_choice) VALUES (%s, %s, %s, "
                "%s, %s, %s)")
            cursor.execute(sql2, (bug_count, project_id, 1, current_datetime, current_datetime, category))
