import { instance } from "./Instance";

async function getTCSheetList(projectId,type = 1) {
    const category = (type === "1")  ? "UI" : "API";
    try {
        const response = await instance.get(`/report/sheetnames?projectid=${projectId}&testCaseCategory=${category}`);
        return response;
    } catch (error) {
        return error.response;
    }
}

async function getTCSheetDetail(sheet, projectId, type = 1) {
    const category = (type === "1")  ? "UI" : "API";
    try {
        const response = await instance.get(`/report/sheet?sheetname=${sheet}&projectid=${projectId}&testCaseCategory=${category}`);
        return response;
    } catch (error) {
        return error.response;
    }
}

async function getTCSheetUpdate(sheet, projectId, data) {
    try {
        const rowData = {
            "rows": data
        }
        const response = await instance.put(`/report/testcase/update?sheetname=${sheet}&projectid=${projectId}`, rowData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export const TestCaseService = {
    getTCSheetList,
    getTCSheetDetail,
    getTCSheetUpdate
};