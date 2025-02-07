import React, { useEffect, useState } from "react";
import { getOrders } from "../services/orderService";
import { Link } from "react-router-dom";

function OrderList() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        getOrders().then(setOrders).catch(console.error);
    }, []);

    return (
        <div>
            <h2>Open Orders</h2>
            <ul>
                {orders.map(order => (
                    <li key={order.lookup_code_order}>
                        {order.lookup_code_order} - {order.status}
                    </li>
                ))}
            </ul>
            <Link to="/create-order">
                <button>Create New Order</button>
            </Link>
        </div>
    );
}

export default OrderList;
