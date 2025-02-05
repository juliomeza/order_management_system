import React, { useEffect, useState } from "react";
import { getOrders } from "../services/orders";

function Orders() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        getOrders().then(setOrders).catch(console.error);
    }, []);

    return (
        <div>
            <h2>Mis Órdenes</h2>
            <ul>
                {orders.map(order => (
                    <li key={order.lookup_code_order}>
                        {order.lookup_code_order} - {order.status}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Orders;
