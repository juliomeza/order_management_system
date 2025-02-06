import API from "../api";
import { jwtDecode } from "jwt-decode";

export const login = async (email, password) => {
    const response = await API.post("/token/", { email, password });

    // Store both access and refresh tokens
    const accessToken = response.data.access;
    const refreshToken = response.data.refresh;

    localStorage.setItem("token", accessToken);        // Store access token
    localStorage.setItem("refresh_token", refreshToken); // Store refresh token

    // Decodificar el access token para obtener el usuario autenticado
    const user = jwtDecode(accessToken);
    localStorage.setItem("user", JSON.stringify(user));

    return response.data;
};

export const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token"); // Clear refresh token on logout as well
    localStorage.removeItem("user");
    window.location.href = "/";
};

export const getUser = () => {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
};

export const isAuthenticated = () => {
    return localStorage.getItem("token") !== null && localStorage.getItem("refresh_token") !== null;
};