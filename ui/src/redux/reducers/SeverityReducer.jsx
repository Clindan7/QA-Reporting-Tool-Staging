import { createSlice } from "@reduxjs/toolkit";

const initialState={
    isLoading:false,
    SeverityData:[],
    errors:{},
}

export const slice=createSlice({
    name:"SeverityChartData",
    initialState,
    reducers:{
        clearSeverityData:()=>initialState,
        setSeverityDataLoading:(state)=>{
            state.isLoading=true;
        },
        setSeverityData:(state,action)=>{
            state.isLoading=false;
            state.SeverityData=action.payload;
        },
        setSeverityError:(state,action)=>{
            state.isLoading=false;
            state.errors=action.payload
        },
        clearSeverityDataError:(state)=>{
            state.isLoading=false;
            state.errors={}
        }
    },
});

export const {clearSeverityData,setSeverityDataLoading,setSeverityData,setSeverityError,clearSeverityDataError} =slice.actions;

export default slice.reducer;