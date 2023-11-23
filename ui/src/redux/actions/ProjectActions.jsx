import { ProjectService } from "../services/ProjectService";
import { toast } from "react-toastify";
import { setDashboardTilesLoading, setDashboardTilesData, setDashboardTilesError } from "../reducers/DashboardReducer";
import { setProjectDetailLoading, setProjectDetailError, setProjectDetailData } from "../reducers/ProjectReducer";
import { setBugDetailData, setBugDetailError, setBugDetailLoading } from "../reducers/BugDetailReducer";
import { setTcDetailData, setTcDetailError, setTcDetailLoading } from "../reducers/TcDetailReducer";

const DashboardTilesAsync = (search, filter) => async (dispatch) => {
  try {
    dispatch(setDashboardTilesLoading());
    const response = await ProjectService.getProjects(search, filter);
    if (response) {
      if (response.status === 200) {
        dispatch(setDashboardTilesData(response?.data?.results));
        dispatch(setDashboardTilesError(""));
      } else {
        dispatch(setDashboardTilesError(response?.data));
        //toast.error(response?.data)
        toast.error("Error in listing")
      }
    }
  } catch (error) {
    dispatch(setDashboardTilesError(error));
    toast.error(error)
  }
};

const ProjectDetailAsync = (id) => async (dispatch) => {
  try {
    dispatch(setProjectDetailLoading());
    const response = await ProjectService.getDetailProject(id);
    if (response?.status ===200) {
      dispatch(setProjectDetailData(response?.data));
      dispatch(setProjectDetailError(''))
    } else {
      dispatch(setProjectDetailData(''));
      dispatch(setProjectDetailError(response))
    }
  } catch (error) {
    dispatch(setProjectDetailError(error))
    toast.error(error)
  }
};

const BugDetailAsync=(id,testCaseCategory)=>async (dispatch)=>{
  try {
    dispatch(setBugDetailLoading());
    const response =await ProjectService.getBugDetail(id,testCaseCategory);
    if(response?.status===200){
      dispatch(setBugDetailData(response?.data))
      dispatch(setProjectDetailError(''))
    }else{
      dispatch(setBugDetailError(response));
      dispatch(setBugDetailData(""))
    }
  } catch (error) {
    dispatch(setBugDetailError(error))
    
  }
}

const TcDetailAsync=(id,testCaseCategory)=> async (dispatch)=>{
  try {
    dispatch(setTcDetailLoading())
    const response =await ProjectService.getTcDetail(id,testCaseCategory);
    if(response?.status===200){
      dispatch(setTcDetailData(response?.data))
      dispatch(setTcDetailError(''))
    }else{
      dispatch(setBugDetailError(response));
      dispatch(setTcDetailData(""))
    }
  } catch (error) {
    dispatch(setBugDetailError(error))
    
  }
}

const ProjectActions = {
  DashboardTilesAsync,
  ProjectDetailAsync,
  BugDetailAsync,
  TcDetailAsync
};
export default ProjectActions