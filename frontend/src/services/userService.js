import API from "./api";

export const getUserProfile = async () => {
    try {
        const response = await API.get("/users/me/");
        return response.data;
    } catch (error) {
        console.error("Error fetching user profile:", error);
        return null;
    }
};
