
import { Navigate, Outlet } from "react-router-dom";
import { appRoutes } from "../pages/app/AppRoutes";
import ErrorPage from "../pages/404/ErrorPage";

export const routes = [
    {
      path: "",
      element: <Outlet />,
  
      children: [
        { index: true, element: <Navigate to="/login" replace /> },
        ...appRoutes,
        {path:"*",element:<ErrorPage />}
      ],
    },
  ];


