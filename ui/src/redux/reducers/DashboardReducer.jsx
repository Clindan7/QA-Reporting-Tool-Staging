import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  isLoading: false,
  DashboardData: {},
  errors: {},
};

export const slice = createSlice({
  name: "dashboardTilesData",
  initialState,
  reducers: {
    clearDashboardTilesData: () => initialState,
    setDashboardTilesLoading: (state) => {
      state.isLoading = true;
    },
    setDashboardTilesData: (state, action) => {
      state.isLoading = false;
      state.DashboardData = action.payload;
    },
    setDashboardTilesError: (state, action) => {
      state.isLoading = false;
      state.errors = action.payload;
    },
    clearDashboardTilesError: (state) => {
      state.isLoading = false;
      state.errors = {};
    }
  },
});

export const { clearDashboardTilesData, setDashboardTilesLoading, setDashboardTilesData, setDashboardTilesError, clearDashboardTilesError } = slice.actions;

export default slice.reducer;