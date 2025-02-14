import API from "./api";

export const getOrders = async () => {
    const response = await API.get("/orders/");
    return response.data;
};

export const createOrder = async (orderData) => {
    const response = await API.post("/orders/", orderData);
    return response.data;
};