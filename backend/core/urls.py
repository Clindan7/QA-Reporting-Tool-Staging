
from django.urls import path, include

urlpatterns = [
    path("users/", include('users.urls')),
    path("project/",include('project.urls')),
    path("report/",include('report.urls'))
]
