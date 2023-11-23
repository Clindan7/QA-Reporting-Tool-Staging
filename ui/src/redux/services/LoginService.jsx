import { instance } from "./Instance";
import { toast } from "react-toastify";

async function getAccessToken(idToken) {
  try {
    const param = {
      "access_token": idToken
    };
    const response = await instance.post("/users/login/",param);
    return response;
  } catch (error) {
    if(error?.response?.status === 500){
      toast.error("Login failed!");
    }
    else if(error.response.data.error_code === 1010){
      toast.error("Access denied!!");
    }
    else if (error.response.data.error_code === 1008){
      toast.error("Unable to extract user info from token.Try again later");
    }
    return error.response;
  }
}


export const LoginService={
    getAccessToken
}