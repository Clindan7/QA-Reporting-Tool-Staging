import React from "react";
import AppLayout from "../../layout/AppLayout";
import { Navigate, Outlet } from "react-router-dom";
import Login from "../login/Login";

const DashBoardPage = React.lazy(() => import("../dashboard/Dashboard"));
const ProjectPage = React.lazy(() => import("../project/Project"));
const TestcasePage = React.lazy(() => import("../testcase/Testcase"))

export const appRoutes = [
  {
    path: "",
    element: <Outlet />,
    children: [
      { index: true, element: <Navigate to="/login" replace /> },
      {
        path: "login",
        element: <Login />,
        name: "Login",
      }
    ],
  },
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/" replace /> },
      {
        path: "dashboard",
        element: <DashBoardPage />,
        name: "Dashboard",
      },
      {
        path: "project/:id",
        element: <ProjectPage />,
        name: "Project",
      },
      {
        path: "project/:id/testcase",
        element: <TestcasePage />,
        name: "Testcase",
      },
    ],
  },
];

