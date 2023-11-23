import axios from "axios";
import { env } from "../../utils/env";

const url = env.API_BASE_URL || '/';

export const instance = axios.create({
    baseURL: url,
    headers: {}
});

instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("accessToken");

    if (token) {
        config.headers["Authorization"] = token;
    }
    return config;
})

instance.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const { config } = error;

        if (error?.response?.status === 401 && !config._retry) {
            config._retry = true;
            try {
                const accessToken = await refreshToken();
                localStorage.setItem("accessToken",accessToken)
                config.headers["Authorization"] = accessToken;
                return axios(config);
            } catch (refreshError) {
                console.error("Token refresh failed:", refreshError);
                handleRefreshTokenError();
            }
        } else if(error?.response?.status===404) {
            window.location.replace("/page-not-found");

        }else {
            return Promise.reject(error);

        }
    }
);

const refreshToken = async () => {
    const refreshToken = localStorage.getItem("refreshToken");
    const data = { "refresh_token": refreshToken };

    try {
        const res = await axios.post(env.API_BASE_URL +"/users/refreshtoken/", data);
        const accessToken = res?.data?.Access_Token;
        localStorage.setItem("accessToken", accessToken);
        return accessToken;
    } catch (error) {
        return Promise.reject(error);
    }
};

const handleRefreshTokenError = () => {
    localStorage.clear();
    window.location.replace("/login");
};
