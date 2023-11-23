import { instance } from "./Instance";

async function serverityReport(id, testCaseCategory) {
  try {
    const res = await instance.get(`report/severity/${id}?testCaseCategory=${testCaseCategory}`);
    return res;
  } catch (error) {
    console.log(error);
  }
}

async function getBugcountReport(id, docType){
    const category = (docType=== "1") ? "UI" : "API";
    try {
       const res= await instance.get(`report/featurewisebug/${id}?testCaseCategory=${category}`) 
       return res;
    } catch (error) {
        console.log(error); 
    }
}

async function testProgressReport(id, testCaseCategory) {
  try {
    const res = await instance.get(`report/testProgress/${id}?testCaseCategory=${testCaseCategory}`);
    return res;
  } catch (error) {
    console.log(error);
  }
}

async function getTestInputData(id, testCaseCategory) {
  try {
    const res = await instance.get(`project/testcaseExecutionCount/${id}?testCaseCategory=${testCaseCategory}`);
    return res;
  } catch (error) {
    console.log(error);
    return error
  }
}

async function updateTestInputData(id, testCaseCategory, data) {
  const category = (testCaseCategory=== "1") ? "UI" : "API";
  try {
    const res = await instance.post(`project/testcaseExecutionCount/update/${id}?testCaseCategory=${category}`,data);
    return res;
  } catch (error) {
    console.log(error);
  }
}

export const chartService ={
    serverityReport,
    getBugcountReport,
    testProgressReport,
    getTestInputData,
    updateTestInputData
}
