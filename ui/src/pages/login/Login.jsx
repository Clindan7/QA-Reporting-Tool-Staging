import "./Login.css";
import loginImage from "../../assets/1.svg";
import googleicon from "../../assets/googleicon.svg";
import Logo from "../../assets/Logo.png"
import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from "react-router-dom";
import LoadingScreen from "../../components/ui/loader/Loader";
import { LoginService } from "../../redux/services/LoginService";


const Login = () => {
  const [isLoading, setIsLoading] = useState(false);
  const Navigate = useNavigate()
  const googleSignIn = useGoogleLogin({
    onSuccess: (res) => {
      setIsLoading(true);
      LoginService.getAccessToken(res.access_token)
        .then((response) => {
          localStorage.setItem("accessToken", response?.data?.Access_Token);
          localStorage.setItem("refreshToken", response?.data?.Refresh_Token);
          localStorage.setItem("username", response?.data?.username);
          Navigate("/dashboard");
        })
        .catch((error) => {
          toast.error(error);
        })
        .finally(() => {
          setIsLoading(false);
        });
    },
    onError: (error) => {
      toast.error(error);
      return error;
    }
  });
  

  useEffect(()=>{
    const roleData = localStorage.getItem("accessToken")
    if(roleData && roleData !== "undefined" ){
      Navigate("/dashboard");
    }
  })

  return (
    <div className="body">
      <div className="mainlogin">
        <div className="imageBox">
          <img className="loginImage" src={loginImage} alt="Login" />
        </div>
        <div className="signIn">
          <div className="logoSection">
            <img src={Logo} alt="" className="logo" />
          </div>
          <div className="signInSection">

            <h3 className="font"> Welcome back you have been missed!</h3>
            <button className="signInButton" onClick={googleSignIn}>
              <div style={{ display: "flex", flexDirection: "row", gap: "20px", marginRight: "auto", justifyContent: "center", alignItems: "center" }}>
                <img src={googleicon} alt="" className="gIcon" />
                <div className="typo">Log in with google</div>
              </div>
            </button>
          </div>
        </div>
      </div>
      {isLoading && <LoadingScreen />}
    </div>
  );
}

export default Login
