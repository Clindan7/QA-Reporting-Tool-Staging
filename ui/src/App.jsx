import { routes } from "./router/RouterConfig";
import { useRoutes } from "react-router-dom";
import { Suspense } from "react";
import { env } from './utils/env.jsx';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import LoadingScreen from "./components/ui/loader/Loader";
function App() {

  const route = useRoutes(routes);
  return (
    <>
      <Suspense fallback={<LoadingScreen />}>
        <GoogleOAuthProvider clientId={env.Client_Id}>
          {route} </GoogleOAuthProvider>
      </Suspense>
      <ToastContainer
        position="top-center"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </>
  )
}

export default App
