from rest_framework import serializers
from report.models.test_cases import TestCaseDateAndCount
from project.models.projects import Projects
from project import project_error 
from datetime import datetime


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = '__all__'

class TestCaseDateAndCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseDateAndCount
        fields = '__all__'

 
   
