import API from "./api";

export const login = async (email, password) => {
    try {
        const response = await API.post("/token/", { email, password });

        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;
        const user = response.data.user;

        localStorage.setItem("token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);
        localStorage.setItem("user", JSON.stringify(user));

        return { user, accessToken };
    } catch (error) {
        console.error("Login error:", error);
        throw error;
    }
};


export const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    window.location.href = "/";
};

export const getUser = () => {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : {};
};

export const isAuthenticated = () => {
    return localStorage.getItem("token") !== null && localStorage.getItem("refresh_token") !== null;
};

