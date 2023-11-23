import pandas as pd
from report.excel_utils import count_actual_result_in_headers, read_excel_file
from report.models.test_cases import SweepBugs, TestCases
from report.models.test_cases import Sweep
import logging
logger = logging.getLogger(__name__)


def process_sheet(sheet_df):
    if "date_of_release" in sheet_df.columns:
        sheet_df["date_of_release"] = pd.to_datetime(
            sheet_df["date_of_release"], format="%d/%m/%Y"
        )
        sheet_df["date_of_release"] = sheet_df["date_of_release"].dt.strftime(
            "%Y-%m-%d"
        )

def fetch_bug_ids(data):
    bug_ids = []
    for key, value in data.items():
        if key.startswith("Bug ID."):
            if key == "Bug ID.0":
                sweep_num = "sweep1"
            elif key == "Bug ID.1.1":
                sweep_num = "sweep2"
            elif key == "Bug ID.2.2":
                sweep_num = "sweep3"
            elif key == "Bug ID.3.3":
                sweep_num = "sweep4"
            else:
                sweep_num = "unknown_sweep"
            
            if isinstance(value, str) and value.strip():
                bug_ids.extend([f"{sweep_num}_{bug_id.strip()}" for bug_id in value.strip().split(",")])
            elif isinstance(value, int):
                bug_ids.append(f"{sweep_num}_{str(value)}")
    return bug_ids


def create_test_case(data, project_id, sweep_count,ui_or_api):
    actual_result_count = sum('Actual Result' in key for key in data.keys())
    print(actual_result_count)
    

    bug_ids = fetch_bug_ids(data)
    test_case = TestCases.objects.create(
        test_case_id=data["test_case_id"],
        description=data["description"],
        feature=data["feature"],
        sub_feature=data["sub_feature"],
        test_steps=data["test_steps"],
        pre_condition=data["pre_condition"],
        expected_results=data["expected_results"],
        category=data["category"],
        status=data["status"],
        comments=data["comments"],
        sheet_name=data["sheet_name"],
        project_id=project_id,
        test_case_choice=ui_or_api
    )

    existing_sweep_records = Sweep.objects.filter(test_cases=test_case)
    if existing_sweep_records:
        Sweep.objects.filter(test_cases=test_case).delete()
    sheet_name = data.get("sheet_name", "")  
    sheet_names = [sheet_name] if sheet_name else [] 
    for sheet in sheet_names:
        for i in range(actual_result_count):        
            actual_result_key = f"Actual Result.{i}"
            build_key = f"Build.{i}"
            sweep_status_key = f"Pass/ Fail.{i}"

            if i == 0:
                actual_result_key = f"Actual Result.{i}"
                build_key = f"Build.{i}"
                sweep_status_key = f"Pass/ Fail.{i}"
                actual_result = str(data.get(actual_result_key, "")).strip()
                build = str(data.get(build_key, "")).strip()
                sweep_status = str(data.get(sweep_status_key, "")).strip()
                Sweep.objects.create(
                    test_cases=test_case,
                    actual_result=actual_result,
                    build=build,
                    sweep_status=sweep_status,
                    sweep_count=i + 1,
                )
                create_sweep_bugs(bug_ids,test_case,i)
            else:
                if i > 0:
                    actual_result_key += f".{i}"
                    build_key += f".{i}"
                    sweep_status_key += f".{i}"
                    actual_result = str(data.get(actual_result_key, "")).strip()
                    build = str(data.get(build_key, "")).strip()
                    sweep_status = str(data.get(sweep_status_key, "")).strip()
                    Sweep.objects.create(
                        test_cases=test_case,
                        actual_result=actual_result,
                        build=build,
                        sweep_status=sweep_status,
                        sweep_count=i + 1,
                    )
                    create_sweep_bugs(bug_ids,test_case,i)
             
                        
def create_sweep_bugs(bug_ids,test_case,i):
    for bug_id_item in bug_ids:
        sweep_number, _, bug_id = bug_id_item.partition('_')
        if sweep_number == f"sweep{i + 1}":
            sweep_obj = Sweep.objects.get(test_cases=test_case, sweep_count=i + 1)
            SweepBugs.objects.create(sweep=sweep_obj, bug_id=bug_id.strip())
