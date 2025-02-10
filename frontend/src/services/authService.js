import API from "./api";

export const login = async (email, password) => {
    try {
        const response = await API.post("/token/", { email, password });

        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;
        const user = response.data.user;

        sessionStorage.setItem("token", accessToken);  // 🔹 Cambiar a sessionStorage
        sessionStorage.setItem("refresh_token", refreshToken);  // 🔹 Cambiar a sessionStorage
        localStorage.setItem("user", JSON.stringify(user));  // 🔹 User se queda en localStorage

        return { user, accessToken };
    } catch (error) {
        console.error("Login error:", error);
        throw error;
    }
};

export const logout = () => {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    window.location.href = "/";
};

export const getUser = () => {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
};

export const isAuthenticated = () => {
    return sessionStorage.getItem("token") !== null && sessionStorage.getItem("refresh_token") !== null;
};
