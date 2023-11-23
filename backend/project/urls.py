from project.views import (get_testcase_count_and_date, list_projects,get_project_by_id,update_testcase_count_and_date)
from django.urls import path

urlpatterns = [
    path('<str:id>', get_project_by_id, name='get_project_by_id'),
    path('listproject/',list_projects),
    path('testcaseExecutionCount/<str:id>',get_testcase_count_and_date),
    path('testcaseExecutionCount/update/<str:id>',update_testcase_count_and_date)
]
