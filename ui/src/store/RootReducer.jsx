import { combineReducers } from "@reduxjs/toolkit";
import ProjectReducer from '../redux/reducers/ProjectReducer';
import DashboardReducer from "../redux/reducers/DashboardReducer";
import TCSheetDetailReducer from "../redux/reducers/TCSheetDetailReducer";
import TCSheetListReducer from "../redux/reducers/TCSheetListReducer";
import fileReducer from "../redux/reducers/fileReducer";
import SeverityReducer from "../redux/reducers/SeverityReducer";
import TCCountInputReducer from "../redux/reducers/TCCountInputReducer";
import TestProgressReducer from "../redux/reducers/TestProgressReducer";
import FeatureTblReducer from "../redux/reducers/FeatureTblReducer";
import BugDetailReducer from "../redux/reducers/BugDetailReducer";
import TcDetailReducer from "../redux/reducers/TcDetailReducer";

const RootReducer = combineReducers({
    ProjectReducer: ProjectReducer,
    DashboardReducer: DashboardReducer,
    TCSheetDetailReducer: TCSheetDetailReducer,
    TCSheetListReducer: TCSheetListReducer,
    FileReducer: fileReducer,
    SeverityReducer: SeverityReducer,
    TCCountInputReducer: TCCountInputReducer,
    TestProgressReducer: TestProgressReducer,
    FeatureTblReducer:FeatureTblReducer,
    BugDetailReducer:BugDetailReducer,
    TcDetailReducer:TcDetailReducer
})

export default RootReducer
