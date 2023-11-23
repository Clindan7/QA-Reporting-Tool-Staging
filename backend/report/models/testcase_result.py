from django.db import models

from project.models.projects import Projects


class TestcaseResult(models.Model):
    version = models.TextField(max_length=255, null=True)
    date_of_release = models.DateField(null=True)
    prepared_by = models.TextField(max_length=255, null=True)
    reviewed_by = models.TextField(max_length=255, null=True)
    approved_by = models.TextField(max_length=255, null=True)
    change_description = models.TextField(
        max_length=255, blank=True, null=True)
    SHEET_CHOICES = ((0, "cover and version"), (1, "amendment of tc"))
    sheet_name = models.CharField(max_length=255, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "testcase_result"
