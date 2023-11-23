# Generated by Django 4.2.5 on 2023-10-13 08:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

USERS_MEMBERS = "users.members"
PROJECT_PROJECTS="project.projects"


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('backlog_category_id', models.IntegerField(null=True, unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='CustomFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=255)),
                ('backlog_custom_id', models.IntegerField(null=True, unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'custom_fields',
            },
        ),
        migrations.CreateModel(
            name='Milestones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('backlog_milestone_id', models.IntegerField(null=True, unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'milestones',
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('project_code', models.CharField(max_length=20, unique=True)),
                ('release_date', models.DateField(default=django.utils.timezone.now)),
                ('notes', models.TextField(blank=True, max_length=255)),
                ('backlog_project_id', models.IntegerField(null=True, unique=True)),
                ('issue_count', models.IntegerField(null=True)),
                ('uat_release', models.DateField(null=True)),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(db_column='updated_by', null=True, on_delete=django.db.models.deletion.CASCADE, to=USERS_MEMBERS)),
            ],
            options={
                'db_table': 'projects',
            },
        ),
        migrations.CreateModel(
            name='Versions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=255, null=True)),
                ('start_date', models.DateField(null=True)),
                ('release_due_date', models.DateField(null=True)),
                ('backlog_version_id', models.IntegerField(null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=PROJECT_PROJECTS)),
            ],
            options={
                'db_table': 'versions',
            },
        ),
        migrations.CreateModel(
            name='SummaryReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_titile', models.CharField(max_length=50)),
                ('testing_cycle', models.CharField(max_length=50)),
                ('testcase_total', models.IntegerField()),
                ('testcase_not_yet', models.IntegerField()),
                ('testcase_passed', models.IntegerField()),
                ('testcase_failed', models.IntegerField()),
                ('tesetcase_blocking', models.IntegerField()),
                ('testcase_not_tested', models.IntegerField()),
                ('developer_issue', models.IntegerField()),
                ('testcase_progress', models.IntegerField()),
                ('remaining_tc', models.IntegerField()),
                ('project_status', models.CharField(max_length=50)),
                ('production_release', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_executed_tc', models.IntegerField()),
                ('total_bugs', models.IntegerField()),
                ('average_bugs', models.IntegerField()),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('milestones', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.milestones')),
            ],
            options={
                'db_table': 'summary_report',
            },
        ),
        migrations.CreateModel(
            name='ProjectsMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_role', models.PositiveSmallIntegerField(choices=[(0, 'admin'), (1, 'project member')], null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=USERS_MEMBERS)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=PROJECT_PROJECTS)),
            ],
            options={
                'db_table': 'projects_members',
            },
        ),
        migrations.CreateModel(
            name='ProjectIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_type', models.CharField(blank=True, max_length=255, null=True)),
                ('subject', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('issue_status', models.CharField(max_length=255, null=True)),
                ('priority', models.CharField(blank=True, max_length=255, null=True)),
                ('milestone', models.CharField(blank=True, max_length=255, null=True)),
                ('issue_start_date', models.DateTimeField(null=True)),
                ('issue_due_date', models.DateTimeField(null=True)),
                ('estimated_hours', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('actual_hours', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('issue_key', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_in_backlog', models.DateTimeField(null=True)),
                ('backlog_issue_id', models.IntegerField(default=None, unique=True)),
                ('status', models.SmallIntegerField(null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_issues', to=USERS_MEMBERS)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.category')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=PROJECT_PROJECTS)),
                ('registered_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registered_issues', to=USERS_MEMBERS)),
                ('updated_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_users', to=USERS_MEMBERS)),
                ('versions', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.versions')),
            ],
            options={
                'db_table': 'project_issues',
            },
        ),
        migrations.CreateModel(
            name='ProjectIssueCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.category')),
                ('project_issues', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.projectissues')),
            ],
            options={
                'db_table': 'projects_issues_categories',
            },
        ),
        migrations.AddField(
            model_name='milestones',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=PROJECT_PROJECTS),
        ),
        migrations.CreateModel(
            name='CustomFieldsIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('custom_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.customfields')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=PROJECT_PROJECTS)),
            ],
            options={
                'db_table': 'custom_fields_issues',
            },
        ),
        migrations.AddField(
            model_name='customfields',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=PROJECT_PROJECTS),
        ),
        migrations.AddField(
            model_name='category',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=PROJECT_PROJECTS),
        ),
    ]