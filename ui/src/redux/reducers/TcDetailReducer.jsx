import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    isLoading: false,
    TcData: {},
    errors: {},
  };

  export const slice=createSlice({
    name:"TcDetailData",
    initialState,
    reducers:{
        clearTcDetailData:()=>initialState,
        setTcDetailLoading:(state)=>{
            state.isLoading=true;
        },
        setTcDetailData:(state,action)=>{
            state.isLoading=false;
            state.TcData=action.payload;
        },
        setTcDetailError:(state,action)=>{
            state.isLoading=false;
            state.errors=action.payload;
        },
        clearTcDetailError:(state)=>{
            state.isLoading=false;
            state.errors={};
        }
    }
  })

  export const {clearTcDetailData,clearTcDetailError,setTcDetailData,setTcDetailError,setTcDetailLoading} =slice.actions;

  export default slice.reducer;