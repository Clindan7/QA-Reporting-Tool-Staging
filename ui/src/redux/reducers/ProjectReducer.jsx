import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  isLoading: false,
  ProjectData: {},
  errors: {},
};

export const slice = createSlice({
  name: "projectDetailData",
  initialState,
  reducers: {
    clearProjectDetailData: () => initialState,
    setProjectDetailLoading: (state) => {
      state.isLoading = true;
    },
    setProjectDetailData: (state, action) => {
      state.isLoading = false;
      state.ProjectData = action.payload;
    },
    setProjectDetailError: (state, action) => {
      state.isLoading = false;
      state.errors = action.payload;
    },
    clearProjectDetailError: (state) => {
      state.isLoading = false;
      state.errors = {};
    }
  },
});

export const { clearProjectDetailData, setProjectDetailLoading, setProjectDetailData, setProjectDetailError, clearProjectDetailError } = slice.actions;

export default slice.reducer;