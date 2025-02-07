import React from "react";
import { useOrders } from "../hooks/useOrders";
import { Link } from "react-router-dom";

function OrderList() {
    const { orders } = useOrders(); // Ahora usa el hook en lugar de llamar directamente a orderService

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
