import { clearDashboardTilesData, clearDashboardTilesError} from '../redux/reducers/DashboardReducer';
import { clearProjectDetailData, clearProjectDetailError} from '../redux/reducers/ProjectReducer';
import {clearImportExportData,clearImportExportError} from "../redux/reducers/fileReducer";
import { clearSeverityData,clearSeverityDataError } from '../redux/reducers/SeverityReducer';

const clearReducers = (dispatch) => {
    localStorage.removeItem("accessToken")
    localStorage.removeItem("refreshToken")
    dispatch(clearDashboardTilesData());
    dispatch(clearDashboardTilesError());
    dispatch(clearProjectDetailData());
    dispatch(clearProjectDetailError());
    dispatch(clearImportExportData());
    dispatch(clearImportExportError());
    dispatch(clearSeverityData());
    dispatch(clearSeverityDataError())
};
 export default clearReducers
