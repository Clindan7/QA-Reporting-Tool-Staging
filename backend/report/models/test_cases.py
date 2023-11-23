from django.db import models
from project.models.projects import Projects
from project.models.projects import ProjectIssues


class TestCases(models.Model):
    test_case_id =  models.TextField(max_length=255, null=True)
    description = models.TextField(max_length=255, null=True)
    feature =  models.TextField(max_length=255, null=True)
    sub_feature =  models.TextField(max_length=255, null=True)
    test_steps = models.TextField(max_length=255, null=True)
    pre_condition = models.TextField(max_length=255, null=True)
    expected_results = models.TextField(max_length=255, null=True)
    category =  models.TextField(max_length=255, null=True)
    STATUS_CHOICES = ((0, "pass"), (1, "fail"))
    status = models.CharField(max_length=50, null=True)
    TEST_CASE_CHOICES = ((0, "api"), (1, "ui"))
    test_case_choice = models.CharField(max_length=50, null=True)
    browser_compatibility = models.ForeignKey(
        "BrowserCompatibility",
        on_delete=models.CASCADE,
        related_name="test_cases_browser_compatibility",
        null=True,
    )
    sheet_name = models.CharField(max_length=50, blank=True, null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    project_issues = models.ForeignKey(
        ProjectIssues, on_delete=models.CASCADE, null=True
    )
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
    comments = models.TextField(null=True)

    class Meta:
        db_table = "test_cases"


class Sweep(models.Model):
    actual_result = models.TextField(null=True)
    build =  models.TextField(max_length=255, null=True)
    SWEEP_COUNT_CHOICES = ((1, "sweep_1"), (2, "sweep_2"), (3, "sweep_3"))
    sweep_count =  models.TextField(max_length=255, null=True)
    SWEEP_STATUS_CHOICES = ((1, "pass"), (2, "fail"), (3, "untested"))
    sweep_status = models.CharField(max_length=50, null=True)
    test_cases = models.ForeignKey(
        "TestCases",
        on_delete=models.CASCADE,
        related_name="sweep_test_cases",
        null=True,
    )
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "sweep"


class SweepBugs(models.Model):
    sweep = models.ForeignKey(
        Sweep, on_delete=models.CASCADE, null=True
    )
    bug_id =  models.TextField(max_length=255, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "sweep_bugs"


class BrowserCompatibility(models.Model):
    TEST_STATUS = ((1, "pass"), (2, "fail"))
    google_chrome_latest = models.PositiveSmallIntegerField(
        choices=TEST_STATUS, null=True
    )
    microsoft_edge_latest = models.PositiveSmallIntegerField(
        choices=TEST_STATUS, null=True
    )
    mac_safari_latest = models.PositiveSmallIntegerField(choices=TEST_STATUS, null=True)
    mac_chrome_latest = models.PositiveSmallIntegerField(choices=TEST_STATUS, null=True)
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        db_table = "browser_compatibility"

class TestCaseDateAndCount(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    excuted_test_case_count = models.IntegerField(null=True)
    passed_test_case_count = models.IntegerField(null=True)
    date_of_executiion = models.DateField(null=True)
    test_case_choice = models.CharField(max_length=50, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
    
    
    class Meta:
        db_table = "test_case_date_count"
    