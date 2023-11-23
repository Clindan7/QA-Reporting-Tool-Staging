from django.urls import path
from report.views import bugs_stats, feature_wise_bug_count_report, import_data_from_summary, export_report, \
    list_all_page_name, list_sheet_details, severity_report, feature_wise_summary_report, test_case_summary, \
    test_progress_report

urlpatterns = [
    path('testcaseImport/<str:project_id>/<str:sweep_count>/<str:ui_or_api>/',import_data_from_summary,name='import_data_from_summary'),
    path('sheetnames',list_all_page_name, name = 'list_all_page_name'),
    path('sheet',list_sheet_details,name = 'list_excel_sheet'),
    path("export/<str:project_id>", export_report, name='export_report'),
    path("severity/<str:project_id>", severity_report, name='severity_report'),
    path("featurewisebug/<str:project_id>",feature_wise_bug_count_report,name='feature_wise_bug_count_report'),
    path("featureWiseSummaryReport/<str:project_id>", feature_wise_summary_report, name='feature_wise_summary_report'),
    path("bugsStats/<str:project_id>", bugs_stats, name='bugs_stats'),
    path("summaryStats/<str:project_id>", test_case_summary, name='test_case_summary'),
    path("testProgress/<str:project_id>", test_progress_report, name='test_progress_report')

]