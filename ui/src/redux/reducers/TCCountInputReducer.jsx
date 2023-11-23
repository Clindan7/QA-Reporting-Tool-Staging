import { createSlice } from "@reduxjs/toolkit";

const initialState={
    isLoading:false,
    TCInputData:{},
    errors:{},
}

export const slice=createSlice({
    name:"TestCaseInputData",
    initialState,
    reducers:{
        clearTCInputData:()=>initialState,
        setTCInputDataLoading:(state)=>{
            state.isLoading=true;
        },
        setTCInputData:(state,action)=>{
            state.isLoading=false;
            state.TCInputData=action.payload;
        },
        setTCInputDataError:(state,action)=>{
            state.isLoading=false;
            state.errors=action.payload
        },
        clearTCInputDataError:(state)=>{
            state.isLoading=false;
            state.errors={}
        }
    },
});

export const {clearTCInputData,setTCInputDataLoading,setTCInputData,setTCInputDataError,clearTCInputDataError} =slice.actions;

export default slice.reducer;