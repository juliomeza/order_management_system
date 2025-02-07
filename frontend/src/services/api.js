import axios from "axios";

const API = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    }
});

// Variable para controlar si hay un refresh en proceso
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    
    failedQueue = [];
};

// Agregar token en cada solicitud
API.interceptors.request.use(config => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Manejar respuestas 401 (token expirado)
API.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Si el error es 401 y no es un retry y no es la ruta de refresh
        if (
            error.response?.status === 401 && 
            !originalRequest._retry &&
            !originalRequest.url?.includes('token/refresh')
        ) {
            if (isRefreshing) {
                // Si ya hay un refresh en proceso, agregar esta petición a la cola
                try {
                    const token = await new Promise((resolve, reject) => {
                        failedQueue.push({ resolve, reject });
                    });
                    originalRequest.headers.Authorization = `Bearer ${token}`;
                    return API(originalRequest);
                } catch (err) {
                    return Promise.reject(err);
                }
            }

            originalRequest._retry = true;
            isRefreshing = true;

            try {
                const refreshToken = localStorage.getItem("refresh_token");
                if (!refreshToken) {
                    throw new Error("No refresh token available");
                }

                // Intentar refrescar el token
                const refreshResponse = await axios.post(
                    `${process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000"}/token/refresh/`,
                    { refresh: refreshToken }
                );

                const newToken = refreshResponse.data.access;
                const newRefreshToken = refreshResponse.data.refresh;
                
                // Guardar ambos tokens
                localStorage.setItem("token", newToken);
                localStorage.setItem("refresh_token", newRefreshToken);
                
                // Actualizar el header de la petición original
                originalRequest.headers.Authorization = `Bearer ${newToken}`;
                
                // Procesar la cola de peticiones fallidas
                processQueue(null, newToken);
                
                return API(originalRequest);
            } catch (refreshError) {
                processQueue(refreshError, null);
                
                // Limpiar almacenamiento y redirigir al login
                localStorage.clear();
                window.location.href = "/";
                
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }

        return Promise.reject(error);
    }
);

export default API;