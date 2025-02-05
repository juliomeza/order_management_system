import API from "../api";

export const getOrders = async () => {
    const response = await API.get("/api/orders/");
    return response.data;
};
