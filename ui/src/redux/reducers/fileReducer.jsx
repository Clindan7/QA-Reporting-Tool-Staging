import { createSlice } from "@reduxjs/toolkit";

const initialState={
    isLoading:false,
    importResponse:{},
    errors:null
}

export const slice=createSlice({
    name:"ImportExportErrors",
    initialState,
    reducers:{
        clearImportExportData:()=>initialState,
        setImportExportLoading:(state)=>{
            state.isLoading=true;
            state.errors={}
        },
        setImportExportError:(state,action)=>{
            state.isLoading=false;
            state.errors=action.payload
        },
        clearImportExportError:(state)=>{
            state.errors=null
        },
        setImportExportResponse:(state,action)=>{
            state.isLoading=false;
            state.importResponse=action.payload
        },
    }
});

export const {clearImportExportData,setImportExportLoading,setImportExportError,clearImportExportError, setImportExportResponse} = slice.actions

export default slice.reducer