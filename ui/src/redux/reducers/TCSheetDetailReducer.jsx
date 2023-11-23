import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    isLoading: false,
    SheetData: {},
    errors: {},
};

export const slice = createSlice({
    name: "sheetDetailData",
    initialState,
    reducers: {
        clearSheetDetailData: () => initialState,
        setSheetDetailLoading: (state) => {
            state.isLoading = true;
        },
        setSheetDetailData: (state, action) => {
            state.isLoading = false;
            state.SheetData = action.payload;
        },
        setSheetDetailError: (state, action) => {
            state.isLoading = false;
            state.errors = action.payload;
        },
        clearSheetDetailError: (state) => {
            state.isLoading = false;
            state.errors = {};
        }
    },
});

export const { clearSheetDetailData, setSheetDetailLoading, setSheetDetailError, setSheetDetailData, clearSheetDetailError } = slice.actions;

export default slice.reducer;