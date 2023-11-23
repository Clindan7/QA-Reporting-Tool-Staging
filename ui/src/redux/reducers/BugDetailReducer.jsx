import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    isLoading: false,
    BugData: {},
    errors: {},
  };

  export const slice=createSlice({
    name:"BugDetailData",
    initialState,
    reducers:{
        clearBugDetailData:()=>initialState,
        setBugDetailLoading:(state)=>{
            state.isLoading=true;
        },
        setBugDetailData:(state,action)=>{
            state.isLoading=false;
            state.BugData=action.payload;
        },
        setBugDetailError:(state,action)=>{
            state.isLoading=false;
            state.errors=action.payload;
        },
        clearBugDetailError:(state)=>{
            state.isLoading=false;
            state.errors={};
        }
    }
  })

  export const {clearBugDetailData,clearBugDetailError,setBugDetailData,setBugDetailError,setBugDetailLoading} =slice.actions;

  export default slice.reducer;