from django.db import models

from project.models.projects import Projects


class Summary(models.Model):
    feature = models.CharField(max_length=50, null=True)
    number_of_testcases = models.IntegerField(null=True)
    executed_testcases_count = models.IntegerField(null=True)
    passed_testcases_count = models.IntegerField(null=True)
    failed_testcases_count = models.IntegerField(null=True)
    not_tested_count = models.IntegerField(null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, default=None,null=True)


    class Meta:
        db_table = "summary"
        
