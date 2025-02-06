import API from "../api";

export const login = async (email, password) => {
    const response = await API.post("/token/", { email, password });

    // Guardar tokens en localStorage
    const accessToken = response.data.access;
    const refreshToken = response.data.refresh;

    localStorage.setItem("token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);

    try {
        // Obtener los datos del usuario autenticado
        const userResponse = await API.get(`/users/me/`);
        const user = userResponse.data;
        
        // Guardar solo el first_name en localStorage
        localStorage.setItem("user", JSON.stringify({ first_name: user.first_name }));

        return { user, accessToken };
    } catch (error) {
        console.error("Error fetching user data:", error);
        throw error;
    }
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