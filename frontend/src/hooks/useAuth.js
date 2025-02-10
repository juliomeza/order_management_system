import { useState, } from "react";
import { isAuthenticated, getUser, login, logout } from "../services/authService";

export function useAuth() {
    const [user, setUser] = useState(getUser() || {});
    const [isLoading] = useState(false);

    const handleLogin = async (email, password) => {
        try {
            const { user } = await login(email, password);
            setUser(user);
            return true;
        } catch (error) {
            return false;
        }
    };

    const handleLogout = () => {
        logout();
        setUser(null);
    };

    return { user, isAuthenticated, isLoading, handleLogin, handleLogout };
}

