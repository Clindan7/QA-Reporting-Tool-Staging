import { createSlice } from "@reduxjs/toolkit";

const initialState={
    isLoading:false,
    TestProgressData:{},
    errors:{},
    UpdatedTCData:{}
}

export const slice=createSlice({
    name:"TestProgressChartData",
    initialState,
    reducers:{
        clearTestProgressData:()=>initialState,
        setTestProgressDataLoading:(state)=>{
            state.isLoading=true;
        },
        setTestProgressData:(state,action)=>{
            state.isLoading=false;
            state.TestProgressData=action.payload;
        },
        setTestProgressDataError:(state,action)=>{
            state.isLoading=false;
            state.errors=action.payload
        },
        clearTestProgressDataError:(state)=>{
            state.isLoading=false;
            state.errors={}
        },
        setUpdatedTCDataResponse:(state,action)=>{
            state.isLoading=false;
            state.UpdatedTCData=action.payload
        }
    },
});

export const {clearTestProgressData,setTestProgressDataLoading,setTestProgressData,setTestProgressDataError,clearTestProgressDataError,setUpdatedTCDataResponse} =slice.actions;

export default slice.reducer;