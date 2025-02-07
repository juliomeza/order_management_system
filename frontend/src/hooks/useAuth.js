import { useState, useEffect } from "react";
import { isAuthenticated, getUser, login, logout } from "../services/authService";

export function useAuth() {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Simula la carga del usuario desde el almacenamiento
        const storedUser = getUser();
        if (storedUser) {
            setUser(storedUser);
        }
        setIsLoading(false);
    }, []);

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
