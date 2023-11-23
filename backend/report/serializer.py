from rest_framework import serializers
from report.models.test_cases import TestCases
from report.models.test_cases import Sweep


class SweepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sweep
        fields = '__all__'

    def to_representation(self, instance):

        data = super(SweepSerializer, self).to_representation(instance)
        if isinstance(int(data['sweep_count']), int):
            return {"sweep" + str(data['sweep_count']): data}


class TestCaseSerializer(serializers.ModelSerializer):
    sweep_test_cases = SweepSerializer(many=True, read_only=True)

    class Meta:
        model = TestCases
        fields = '__all__'

    def to_representation(self, instance):

        data = super(TestCaseSerializer, self).to_representation(instance)
        body = {
            "id": data['id'],
            "test_case_id": data['test_case_id'],
            "description": data['description'],
            "feature": data['feature'],
            "sub_feature": data['sub_feature'],
            "test_steps": data['test_steps'],
            "pre_condition": data['pre_condition'],
            "expected_results": data['expected_results'],
            "category": data['category'],
            "status": data['status'],
            "sheet_name": data['sheet_name'],
            "comments": data['comments'],
            "browser_compatibility": data['browser_compatibility'],
            "project_id": data['project']




        }
        sweep = data['sweep_test_cases']
        for element in sweep:
            body.update(element)
        return body
