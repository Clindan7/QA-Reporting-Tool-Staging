from django.db import models
from unittest.mock import patch
from django.utils import timezone

from project.models import Projects


@patch("report.models.BatchProcess.objects.create")
class BatchProcess(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    STATUS_CHOICES = ((1, "active"), (2, "inactive"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(null=True, auto_now_add=True)
    update_date = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = "batch_process"


@patch("report.models.BatchProcess.objects.create")
class SubBatchProcess(models.Model):
    batch_process = models.ForeignKey(BatchProcess, on_delete=models.CASCADE, null=True)
    STATUS_CHOICES = ((1, "active"), (2, "inactive"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    create_date = models.DateTimeField(null=True,auto_now_add=True)
    update_date = models.DateTimeField(null=True,auto_now=True)

    class Meta:
        db_table = "sub_batch_process"


@patch("report.models.BatchProcess.objects.create")
class BugSummary(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    open_bugs = models.CharField(max_length=250, blank=True, null=True)
    TEST_CASE_CHOICES = ((0, "api"), (1, "ui"))
    test_case_choice = models.CharField(max_length=50, null=True)
    STATUS_CHOICES = ((1, "active"), (2, "inactive"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    create_date = models.DateTimeField(null=True,auto_now_add=True)
    update_date = models.DateTimeField(null=True,auto_now=True)

    class Meta:
        db_table = "bug_summary"



