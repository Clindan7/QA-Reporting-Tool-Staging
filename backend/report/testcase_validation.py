error_codes = {
    "test_case_id": 1105,
    "description": 1106,
    "feature": 1107,
    "sub_feature": 1108,
    "test_steps": 1109,
    "expected_results": 1110,
    "status": 1111,
}
status_list = ["Pass", "Fail", "Not Tested"]


def validate_field(value, field_name, row_number, sheet_name):
    if field_name != "status" and (not isinstance(value, str) or not value.strip()):
        error_code = error_codes.get(field_name, 1000)
        return {
            "error_code": error_code,
            "message": f"[Sheet: {sheet_name}, Row: {row_number}] Invalid or empty value '{value}' for '{field_name.capitalize()}', it should be a non-empty string.",
        }

    if field_name == "test_case_id" and not value.startswith("TC_"):
        error_code = error_codes.get(field_name, 1000)
        return {
            "error_code": error_code,
            "message": f"[Sheet: {sheet_name}, Row: {row_number}] Invalid or empty value '{value}' for '{field_name.capitalize()}', Test case Id should start with TC_.",
        }

    if field_name == "status" and value.strip() and value not in status_list:
                error_code = error_codes.get(field_name, 1000)
                return {
                    "error_code": error_code,
                    "message": f"[Sheet: {sheet_name}, Row: {row_number}] Invalid status '{value}' for '{field_name.capitalize()}'. Valid statuses are: {', '.join(status_list)}.",
                }
    return None


def testcase_validation(
    test_case_id,
    feature,
    status,
    row_number,
    sheet_name,
    error_dict,
):
    errors = {}

    test_case_id_error = validate_field(
        test_case_id, "test_case_id", row_number, sheet_name
    )
    if test_case_id_error:
        errors["test_case_id"] = test_case_id_error

    feature_error = validate_field(feature, "feature", row_number, sheet_name)
    if feature_error:
        errors["feature"] = feature_error

    status_error = validate_field(status, "status", row_number, sheet_name)
    if status_error:
        errors["status"] = status_error

    if errors:
        error_dict["errors"] = errors
        return error_dict
    else:
        return None
