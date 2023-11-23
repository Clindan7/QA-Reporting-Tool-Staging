from project import project_error
from .utils import CustomException
import datetime

import datetime


class EditProjectDetailsValidation:
    def validate_project_data(self, data):
        allowed_fields = [
            'notes',
            'uat_release',
            'status',
            'release_date',
            'remarks',
            'risk',
            'start_date'

        ]

        for field in data:
            if field not in allowed_fields:
                raise CustomException(project_error.INVALID_FIELD)

        self.validate_data_types(data)

        if "notes" in data:
            self.validate_notes(data.get("notes"))
        if "uat_release" in data:
            self.date_validator(data.get("uat_release"))
        if "release_date" in data:
            self.date_validator(data.get("release_date"))
        if "status" in data:
            self.status_validator(data.get("status"))
        if "remarks" in data and "status" in data == 0:
            self.remarks_validator(data.get("remarks"))
        if "risk" in data:
            self.risks_validator(data.get("risk"))
        if 'start_date' in data:
            self.date_validator(data.get("start_date"))

    def validate_data_types(self, data):
        expected_types = {
            'notes': str,
            'uat_release': str,
            'release_date': str,
            'status': (int)
        }
        for field, expected_type in expected_types.items():
            value = data.get(field)
            if value is not None and not isinstance(value, expected_type):
                raise CustomException(project_error.INVALID_DATA_TYPE)

    def validate_notes(self, data):
        if len(data) > 100:
            raise CustomException(project_error.NOTES_MAX_LENGTH_ERROR)

    def date_validator(self, data):
        try:
            datetime.date.fromisoformat(str(data))
        except ValueError:
            raise CustomException(project_error.DATE_ERROR)

    def status_validator(self, data):
        if data not in [0, 1]:
            raise CustomException(project_error.STATUS_ERROR)

    def remarks_validator(self, data):
        if len(data) < 4:
            raise CustomException(project_error.REMARKS_MIN_LENGTH_ERROR)
        if len(data) > 100:
            raise CustomException(project_error.REMARKS_MAX_LENGTH_ERROR)

    def risks_validator(self, data):
        if len(data) > 100:
            raise CustomException(project_error.RISKS_MAX_LENGTH_ERROR)


class EditTestCaseExecutionCount():
    def validate_data_types(self, data):
        allowed_fields = [
            'executed_test_case_count',
            'passed_test_case_count',
            'date_of_execution',
            'project'
        ]

        for field in data:
            if field not in allowed_fields:
                raise CustomException(project_error.INVALID_FIELD)
        if "excuted_test_case_count" in data:
            self.excuted_test_case_count(data.get("excuted_test_case_count"))
        if "passed_test_case_count" in data:
            self.excuted_test_case_count(data.get("passed_test_case_count"))
    def excuted_test_case_count(self, data):
        if len(str(data)) > 9:
            raise CustomException(project_error.MAXIMUM_NUMBER_OF_TC)
        try:
            num = int(data)
            if num < 0:
                raise CustomException(project_error.INVALID_DATA_TYPE)
            
            return True 
        except Exception:
            raise CustomException(project_error.INVALID_DATA_TYPE)

