import { useState, useEffect } from "react";
import { isAuthenticated, getUser, login, logout } from "../services/authService";

export function useAuth() {
    const [user, setUser] = useState(getUser());

    useEffect(() => {
        setUser(getUser()); // Asegura que el estado se sincronice con el almacenamiento local
    }, []);

    const handleLogin = async (email, password) => {
        try {
            const { user } = await login(email, password);
            setUser(user);
            return true; // Indica éxito
        } catch (error) {
            return false; // Indica error en autenticación
        }
    };

    const handleLogout = () => {
        logout();
        setUser(null);
    };

    return { user, isAuthenticated, handleLogin, handleLogout };
}
