from django.db import models
from django.utils import timezone
from users.models.members import Members


class Projects(models.Model):
    name = models.CharField(max_length=50)
    project_code = models.CharField(max_length=20, unique=True)
    release_date = models.DateField(default=timezone.now, null=False)
    notes = models.TextField(max_length=255, blank=True)
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    backlog_project_id = models.IntegerField(null=True, unique=True)
    start_date = models.DateField(null=True)
    uat_release = models.DateField(null=True)
    risk = (models.CharField(max_length=255, null=True,blank=True))
    remarks = models.CharField(max_length=255, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    updated_by = models.ForeignKey(
        Members, on_delete=models.CASCADE, null=True, db_column="updated_by"
    )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"


class ProjectsMembers(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    MEMBER_CHOICE = ((0, "admin"), (1, "project member"))
    member_role = models.PositiveSmallIntegerField(choices=MEMBER_CHOICE, null=True)
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects_members"


class Category(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    backlog_category_id = models.IntegerField(unique=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"


class Versions(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    description = models.TextField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    release_due_date = models.DateField(null=True)
    backlog_version_id = models.IntegerField(null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "versions"


class Milestones(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    backlog_milestone_id = models.IntegerField(null=True, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "milestones"


class CustomFields(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    backlog_custom_id = models.IntegerField(null=True, unique=True)

    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "custom_fields"


class CustomFieldsIssues(models.Model):
    custom_field = models.ForeignKey(CustomFields, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "custom_fields_issues"


class ProjectIssues(models.Model):
    issue_type = models.CharField(max_length=255, null=True, blank=True)
    subject = models.TextField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    issue_status = models.CharField(null=True, max_length=255)
    assignee = models.ForeignKey(
        Members,
        on_delete=models.CASCADE,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )
    priority = models.CharField(null=True, max_length=255, blank=True)
    registered_user = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name="registered_issues", null=True
    )
    milestone = models.CharField(null=True, blank=True, max_length=255)
    versions = models.ForeignKey(Versions, on_delete=models.CASCADE, null=True)
    issue_start_date = models.DateTimeField(null=True)
    issue_due_date = models.DateTimeField(null=True)
    estimated_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    actual_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    issue_key = models.CharField(max_length=50, null=True, blank=True)
    updated_user = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name="updated_users", null=True
    )
    created_in_backlog = models.DateTimeField(default=timezone.now, null=True)
    updated_in_backlog = models.DateTimeField(null=True)
    backlog_issue_id = models.IntegerField(null=False, unique=True, default=None)
    status = models.SmallIntegerField(null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)



    class Meta:
        db_table = "project_issues"


class ProjectIssueCategories(models.Model):
    project_issues = models.ForeignKey(
        ProjectIssues, on_delete=models.CASCADE, null=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "projects_issues_categories"
