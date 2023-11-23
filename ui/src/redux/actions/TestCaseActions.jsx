import { TestCaseService } from "../services/TestCaseService";
import { toast } from "react-toastify";
import { setTCSheetListLoading, setTCSheetListData, setTCSheetListError } from "../reducers/TCSheetListReducer";
import { setSheetDetailLoading, setSheetDetailError, setSheetDetailData } from "../reducers/TCSheetDetailReducer";

const SheetListAsync = (projectId, type) => async (dispatch) => {
    try {
        dispatch(setTCSheetListData([]));
        dispatch(setSheetDetailData([]));
        dispatch(setTCSheetListLoading());
        const response = await TestCaseService.getTCSheetList(projectId,type);
        if (response) {
            if (response.status === 200) {
                dispatch(setTCSheetListData(response?.data?.sheet_names));
                dispatch(setTCSheetListError(""));
            } else {
                if(response?.data?.error_code !== 1100){
                    toast.error("Error in loading the document!");
                }
                dispatch(setTCSheetListError(response?.data));
                dispatch(setTCSheetListData([]));
            }
        }
    } catch (error) {
        dispatch(setTCSheetListError(error));
        toast.error(error)
    }
};

const SheetDetailAsync = (sheetName, projectId, type) => async (dispatch) => {
    try {
        dispatch(setSheetDetailLoading());
        const response = await TestCaseService.getTCSheetDetail(sheetName, projectId, type);
        if (response) {
            if (response?.status === 200) {
                dispatch(setSheetDetailData(response?.data?.data));
                dispatch(setSheetDetailError(''))
            } else {
                dispatch(setSheetDetailData([]));
                dispatch(setSheetDetailError(response));
            }
        }
    } catch (error) {
        dispatch(setSheetDetailError(error))
        toast.error(error)
    }
};


const TestCaseActions = {
    SheetListAsync,
    SheetDetailAsync
};
export default TestCaseActions