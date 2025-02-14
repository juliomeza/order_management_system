import { useState, } from "react";
import { isAuthenticated, getUser, login, logout } from "../services/authService";

export function useAuth() {
    const [user, setUser] = useState(getUser() || null);  // 🔹 Cambiamos {} por null
    const [isLoading, setIsLoading] = useState(false);  // 🔹 Ahora es un estado real

    const handleLogin = async (email, password) => {
        setIsLoading(true);
        try {
            const { user } = await login(email, password);
            setUser(user);
            return true;
        } catch (error) {
            return false;
        } finally {
            setIsLoading(false);
        }
    };

    const handleLogout = () => {
        logout();
        setUser(null);
    };

    return { user, isAuthenticated, isLoading, handleLogin, handleLogout };
}
