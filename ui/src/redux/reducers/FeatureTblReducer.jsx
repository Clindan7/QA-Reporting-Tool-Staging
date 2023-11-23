import { createSlice } from "@reduxjs/toolkit";

const initialState={
    isLoading:false,
    tableData:{},
    errors:{}
}

export const slice=createSlice({
    name:"featureTableData",
    initialState,
    reducers:{
        clearFeatureTblData:()=>initialState,
        setFeatureTblDataLoading:(state)=>{
            state.isLoading=true;
        },
        setFeatureTblData:(state,action)=>{
            state.isLoading=false;
            state.tableData=action.payload;
        },
        setFeatureTblError:(state,action)=>{
            state.isLoading=false;
            state.errors=action.payload
        },
        clearFeatureTblError:(state)=>{
            state.isLoading=false;
            state.errors={}
        }
    }
});

export const {clearFeatureTblData,setFeatureTblData,setFeatureTblDataLoading,setFeatureTblError} =slice.actions;

export default slice.reducer;