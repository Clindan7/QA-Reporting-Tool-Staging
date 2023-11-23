from django.db import models
from django.utils import timezone
from project.models.projects import Milestones


class SummaryReport(models.Model):
    project_titile = models.CharField(max_length=50)
    testing_cycle = models.CharField(max_length=50)
    testcase_total = models.IntegerField()
    testcase_not_yet = models.IntegerField()
    testcase_passed = models.IntegerField()
    testcase_failed = models.IntegerField()
    tesetcase_blocking = models.IntegerField()
    testcase_not_tested = models.IntegerField()
    developer_issue = models.IntegerField()
    testcase_progress = models.IntegerField()
    remaining_tc = models.IntegerField()
    project_status = models.CharField(max_length=50)
    production_release = models.DateTimeField(default=timezone.now)
    total_executed_tc = models.IntegerField()
    total_bugs = models.IntegerField()
    milestones = models.ForeignKey(Milestones, on_delete=models.CASCADE)
    average_bugs = models.IntegerField()
    STATUS_CHOICES = ((0, "inactive"), (1, "Active"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "summary_report"
        
