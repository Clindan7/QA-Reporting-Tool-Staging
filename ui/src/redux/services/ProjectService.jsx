import { instance } from "./Instance";

async function getProjects(searchParam, filterParam) {
  const encodedParam = encodeURIComponent(searchParam)
  try {
    const response = await instance.get(`/project/listproject/?search=${encodedParam}&order_by=&page=1&status=${filterParam}`);
    return response;
  } catch (error) {
    return error.response;
  }
}

async function getDetailProject(id) {
  try {
    const response = await instance.get("/project/" + id);
    return response
  } catch (error) {
    return error
  }
}

async function editProjectDetail(id,data){
  try{
    const response=await instance.put(`/project/${id}`,data)
    return response;
  }catch(error){
    return error
  }
}

async function getBugDetail(id,testCaseCategory){
  try {
    const response=await instance.get(`/report/bugsStats/${id}?testCaseCategory=${testCaseCategory}`)
    return response
  } catch (error) {
    return error
  }
}

async function getTcDetail(id,testCaseCategory){
  try {
    const response=await instance.get(`/report/summaryStats/${id}?testCaseCategory=${testCaseCategory}`)
    return response
  } catch (error) {
    return error
  }
}

export const ProjectService = {
  getProjects,
  getDetailProject,
  editProjectDetail,
  getBugDetail,
  getTcDetail
};
