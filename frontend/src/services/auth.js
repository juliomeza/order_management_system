import API from "../api";
import { jwtDecode } from "jwt-decode";

export const login = async (email, password) => {
    const response = await API.post("/token/", { email, password });

    const token = response.data.access;
    localStorage.setItem("token", token);

    // Decodificar el token para obtener el usuario autenticado
    const user = jwtDecode(token);
    localStorage.setItem("user", JSON.stringify(user));

    return response.data;
};

export const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/";
};

export const getUser = () => {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
};

export const isAuthenticated = () => {
    return localStorage.getItem("token") !== null;
};
