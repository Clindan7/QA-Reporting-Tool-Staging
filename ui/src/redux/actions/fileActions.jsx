import { fileService } from "../services/fileService";
import { setImportExportError,setImportExportLoading, setImportExportResponse, clearImportExportError } from "../reducers/fileReducer";
import { toast } from "react-toastify";


const ImportExportAsync = (file, id, docType, sweepCount) => async (dispatch) => {
    try {
        dispatch(setImportExportLoading());
        dispatch(clearImportExportError())
        const response = await fileService.fileImport(file, id, docType, sweepCount);
        if (response.status === 200) {
            toast.success(response?.data?.message)
            dispatch(setImportExportResponse(response?.data))
            dispatch(clearImportExportError())
        } else {
            dispatch(setImportExportError(response?.data));
        }
    } catch (error) {
        dispatch(setImportExportError(error));
    }
};


const fileActions={
    ImportExportAsync
}

export default fileActions;