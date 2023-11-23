import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    isLoading: false,
    TCSheetList: [],
    errors: {},
};

export const slice = createSlice({
    name: "tcSheetListData",
    initialState,
    reducers: {
        clearTCSheetListData: () => initialState,
        setTCSheetListLoading: (state) => {
            state.isLoading = true;
        },
        setTCSheetListData: (state, action) => {
            state.isLoading = false;
            state.TCSheetList = action.payload;
        },
        setTCSheetListError: (state, action) => {
            state.isLoading = false;
            state.errors = action.payload;
        },
        clearTCSheetListError: (state) => {
            state.isLoading = false;
            state.errors = {};
        }
    },
});

export const { clearTCSheetListData, setTCSheetListLoading, setTCSheetListData, setTCSheetListError, clearTCSheetListError } = slice.actions;

export default slice.reducer;