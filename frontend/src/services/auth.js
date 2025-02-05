import API from "../api";

export const login = async (email, password) => {
    const response = await API.post("/api/token/", { email, password });
    localStorage.setItem("token", response.data.access);
    return response.data;
};

export const logout = () => {
    localStorage.removeItem("token");
};
