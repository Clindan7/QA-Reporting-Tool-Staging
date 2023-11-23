import { TableService } from "../services/TableService";
import { setFeatureTblDataLoading,setFeatureTblData,setFeatureTblError } from "../reducers/FeatureTblReducer";
import { toast } from "react-toastify";

const FeatureTableAsync=(id,testCaseCategory)=>async (dispatch)=>{
    try {
        dispatch(setFeatureTblDataLoading())
        const response =await TableService.FeatureTable(id,testCaseCategory);
        if (response?.status===200){
            dispatch(setFeatureTblData(response?.data))
        }else{
            toast.error("Failed to get Feature wise table")
        }
    } catch (error) {
        dispatch(setFeatureTblError(error));
        toast.error("An error occured while fetching feature wise table")
        
    }
}


const TableActions ={
    FeatureTableAsync
}

export default TableActions;