import axios from "axios";

const API = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    }
});

// Variable para controlar si hay un refresh en proceso
let failedQueue = [];
let showSessionExpiredModal = false;

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
    const token = sessionStorage.getItem("token");  // 🔹 Cambiar a sessionStorage
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
        const refreshToken = sessionStorage.getItem("refresh_token");  // 🔹 Cambiar a sessionStorage

        if (
            error.response?.status === 401 &&
            !originalRequest._retry &&
            refreshToken &&  
            !originalRequest.url?.includes('token/refresh')
        ) {
            originalRequest._retry = true;

            try {
                const refreshResponse = await axios.post(
                    `${process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000"}/token/refresh/`,
                    { refresh: refreshToken }
                );

                const newToken = refreshResponse.data.access;
                const newRefreshToken = refreshResponse.data.refresh;
                
                sessionStorage.setItem("token", newToken);
                sessionStorage.setItem("refresh_token", newRefreshToken);
                
                originalRequest.headers.Authorization = `Bearer ${newToken}`;
                processQueue(null, newToken);
                
                return API(originalRequest);
            } catch (refreshError) {
                processQueue(refreshError, null);

                if (!showSessionExpiredModal) {
                    showSessionExpiredModal = true;
                    showModalAndRedirect();
                }

                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);


function showModalAndRedirect() {
    const modal = document.createElement("div");
    modal.style.position = "fixed";
    modal.style.top = "0";
    modal.style.left = "0";
    modal.style.width = "100%";
    modal.style.height = "100%";
    modal.style.background = "rgba(0,0,0,0.5)";
    modal.style.display = "flex";
    modal.style.justifyContent = "center";
    modal.style.alignItems = "center";
    modal.style.zIndex = "1000";

    const modalContent = document.createElement("div");
    modalContent.style.background = "white";
    modalContent.style.padding = "20px";
    modalContent.style.borderRadius = "8px";
    modalContent.style.textAlign = "center";

    const message = document.createElement("p");
    message.innerText = "Your session has expired. Please log in again.";

    const button = document.createElement("button");
    button.innerText = "OK";
    button.style.marginTop = "10px";
    button.onclick = () => {
        modal.remove();
        sessionStorage.clear();
        window.location.href = "/";
    };

    modalContent.appendChild(message);
    modalContent.appendChild(button);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
}

export default API;
