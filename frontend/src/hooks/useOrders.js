import { useState, useEffect } from "react";
import { getOrders, createOrder } from "../services/orderService";

export function useOrders() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = async () => {
        try {
            const data = await getOrders();
            setOrders(data);
        } catch (error) {
            console.error("Error fetching orders:", error);
        }
    };

    const addOrder = async (orderData) => {
        try {
            await createOrder(orderData);
            fetchOrders();
        } catch (error) {
            console.error("Error creating order:", error);
        }
    };

    return { orders, fetchOrders, addOrder };
}
