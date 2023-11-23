import { Navigate, Outlet } from "react-router-dom";
import Header from "../components/ui/header/Header";
import Sidebar from "../components/ui/sidebar/Sidebar";
import '../index.css';

function AppLayout() {
    const roleData = localStorage.getItem("accessToken")
    return (
        <>
            {
                roleData && roleData !== "undefined" ? (
                    <>
                        <Header />
                        <div className="row d-flex">
                            <div className="col-md-2 backgrnd"><Sidebar /></div>
                            <div className="col-md-10 backgrnd"> 
                                <main className="main" data-testid="main"><Outlet /></main>
                            </div>

                        </div>

                    </>
                ) : (
                    <Navigate to="/login" />
                )
            }
        </>
    );
}

export default AppLayout;   