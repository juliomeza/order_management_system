import React, { useEffect, useState } from "react";
import { getOrders, createOrder } from "../services/orders";

function Orders() {
    const [orders, setOrders] = useState([]);
    const [formData, setFormData] = useState({
        lookup_code_order: "",
        lookup_code_shipment: "",
        status: "",
        order_type: "",
        order_class: "",
        project: "",
        warehouse: "",
        contact: "",
        shipping_address: "",
        billing_address: "",
        carrier: "",
        service_type: "",
        expected_delivery_date: "",
        notes: "",
        lines: [{ material: "", quantity: "" }]
    });

    useEffect(() => {
        getOrders().then(setOrders).catch(console.error);
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleLineChange = (index, e) => {
        const newLines = [...formData.lines];
        newLines[index][e.target.name] = e.target.value;
        setFormData({ ...formData, lines: newLines });
    };

    const addLine = () => {
        setFormData({ ...formData, lines: [...formData.lines, { material: "", quantity: "" }] });
    };

    const removeLine = (index) => {
        const newLines = formData.lines.filter((_, i) => i !== index);
        setFormData({ ...formData, lines: newLines });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const newOrder = await createOrder(formData);
            setOrders([...orders, newOrder]); // Agregar la nueva orden a la lista
            setFormData({ // Reiniciar formulario
                lookup_code_order: "",
                lookup_code_shipment: "",
                status: "",
                order_type: "",
                order_class: "",
                project: "",
                warehouse: "",
                contact: "",
                shipping_address: "",
                billing_address: "",
                carrier: "",
                service_type: "",
                expected_delivery_date: "",
                notes: "",
                lines: [{ material: "", quantity: "" }]
            });
        } catch (error) {
            console.error("Error creando la orden:", error);
        }
    };

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

            <h3>Crear Nueva Orden</h3>
            <form onSubmit={handleSubmit}>
                <input type="text" name="lookup_code_order" placeholder="Código de Orden" value={formData.lookup_code_order} onChange={handleChange} required />
                <input type="text" name="lookup_code_shipment" placeholder="Código de Envío" value={formData.lookup_code_shipment} onChange={handleChange} required />
                <input type="number" name="status" placeholder="Estado" value={formData.status} onChange={handleChange} required />
                <input type="number" name="order_type" placeholder="Tipo de Orden" value={formData.order_type} onChange={handleChange} required />
                <input type="number" name="order_class" placeholder="Clase de Orden" value={formData.order_class} onChange={handleChange} required />
                <input type="number" name="project" placeholder="Proyecto" value={formData.project} onChange={handleChange} required />
                <input type="number" name="warehouse" placeholder="Almacén" value={formData.warehouse} onChange={handleChange} required />
                <input type="number" name="contact" placeholder="Contacto" value={formData.contact} onChange={handleChange} required />
                <input type="number" name="shipping_address" placeholder="Dirección de Envío" value={formData.shipping_address} onChange={handleChange} required />
                <input type="number" name="billing_address" placeholder="Dirección de Facturación" value={formData.billing_address} onChange={handleChange} required />
                <input type="number" name="carrier" placeholder="Transportista" value={formData.carrier} onChange={handleChange} />
                <input type="number" name="service_type" placeholder="Tipo de Servicio" value={formData.service_type} onChange={handleChange} />
                <input type="date" name="expected_delivery_date" placeholder="Fecha de Entrega" value={formData.expected_delivery_date} onChange={handleChange} />
                <textarea name="notes" placeholder="Notas" value={formData.notes} onChange={handleChange}></textarea>

                <h4>Líneas de la Orden</h4>
                {formData.lines.map((line, index) => (
                    <div key={index}>
                        <input type="text" name="material" placeholder="Material" value={line.material} onChange={(e) => handleLineChange(index, e)} required />
                        <input type="number" name="quantity" placeholder="Cantidad" value={line.quantity} onChange={(e) => handleLineChange(index, e)} required />
                        <button type="button" onClick={() => removeLine(index)}>Eliminar</button>
                    </div>
                ))}
                <button type="button" onClick={addLine}>Agregar Línea</button>

                <button type="submit">Crear Orden</button>
            </form>
        </div>
    );
}

export default Orders;
