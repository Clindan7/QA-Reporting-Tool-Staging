import { chartService } from "../services/ChartService";
import { setSeverityDataLoading, setSeverityData, setSeverityError } from "../reducers/SeverityReducer";
import { setTCInputDataLoading, setTCInputData, setTCInputDataError } from "../reducers/TCCountInputReducer";
import { setTestProgressDataLoading, setTestProgressData, setTestProgressDataError } from "../reducers/TestProgressReducer";
import { toast } from "react-toastify";

const SeverityChartAsync = (id, testCaseCategory) => async (dispatch) => {
  try {
    dispatch(setSeverityDataLoading());
    const response = await chartService.serverityReport(id, testCaseCategory);
    if (response?.status === 200) {
      dispatch(setSeverityData(response?.data));
    } else {
      dispatch(setSeverityError(response?.status));
      toast.error("Failed to get Feature wise bug count!")
    }
  } catch (error) {
    dispatch(setSeverityError(error));
    toast.error("An error occurred while fetching Feature wise bug count");
  }
}

const TestInputDataAsync = (id, testCaseCategory) => async (dispatch) => {
  try {
    dispatch(setTCInputDataLoading());
    dispatch(setTCInputData([]));
    const response = await chartService.getTestInputData(id, testCaseCategory);
    if (response?.status === 200) {
      dispatch(setTCInputData(response.data));
      dispatch(setTCInputDataError({}));
    }
    else {
      dispatch(setTCInputDataError(response?.status));
      toast.error("Failed to get Test progress Input data!")
    }
  } catch (error) {
    dispatch(setTCInputDataError(error));
  }
}
const TestProgressChartAsync = (id, testCaseCategory) => async (dispatch) => {
  try {
    dispatch(setTestProgressDataLoading());
    const response = await chartService.testProgressReport(id, testCaseCategory);
    if (response?.status === 200) {
      dispatch(setTestProgressData(response.data));
      dispatch(setTestProgressDataError({}));
    }
    else {
      dispatch(setTestProgressDataError(response?.status));
      toast.error("Failed to get Test progress report!")
    }
  } catch (error) {
    dispatch(setTestProgressDataError(error));
  }
}

const ChartActions = {
  SeverityChartAsync,
  TestInputDataAsync,
  TestProgressChartAsync
}

export default ChartActions;
