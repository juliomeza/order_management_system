import React, { useState } from "react";
import { createOrder } from "../services/orders";
import { useNavigate } from "react-router-dom";

function OrderForm() {
    const navigate = useNavigate();
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
            await createOrder(formData);
            navigate("/orders"); // Redirigir a la lista de órdenes
        } catch (error) {
            console.error("Error creando la orden:", error);
        }
    };

    return (
        <div>
            <h3>Create New Order</h3>
            <form onSubmit={handleSubmit}>
                <input type="text" name="lookup_code_order" placeholder="Order Number" value={formData.lookup_code_order} onChange={handleChange} required />
                <input type="text" name="lookup_code_shipment" placeholder="Shipment Number" value={formData.lookup_code_shipment} onChange={handleChange} required />
                <input type="number" name="status" placeholder="Status" value={formData.status} onChange={handleChange} required />
                <input type="number" name="order_type" placeholder="Order Type" value={formData.order_type} onChange={handleChange} required />
                <input type="number" name="order_class" placeholder="Order Class" value={formData.order_class} onChange={handleChange} required />
                <input type="number" name="project" placeholder="Project" value={formData.project} onChange={handleChange} required />
                <input type="number" name="warehouse" placeholder="Warehouse" value={formData.warehouse} onChange={handleChange} required />
                <input type="number" name="contact" placeholder="Contact" value={formData.contact} onChange={handleChange} required />
                <input type="number" name="shipping_address" placeholder="Shipping Address" value={formData.shipping_address} onChange={handleChange} required />
                <input type="number" name="billing_address" placeholder="Billing Address" value={formData.billing_address} onChange={handleChange} required />
                <input type="number" name="carrier" placeholder="Carrier" value={formData.carrier} onChange={handleChange} />
                <input type="number" name="service_type" placeholder="Service" value={formData.service_type} onChange={handleChange} />
                <input type="date" name="expected_delivery_date" placeholder="Expected Delivery Date" value={formData.expected_delivery_date} onChange={handleChange} />
                <textarea name="notes" placeholder="Notes" value={formData.notes} onChange={handleChange}></textarea>

                <h4>Order Lines</h4>
                {formData.lines.map((line, index) => (
                    <div key={index}>
                        <input type="text" name="material" placeholder="Material" value={line.material} onChange={(e) => handleLineChange(index, e)} required />
                        <input type="number" name="quantity" placeholder="Quantity" value={line.quantity} onChange={(e) => handleLineChange(index, e)} required />
                        <button type="button" onClick={() => removeLine(index)}>Delete</button>
                    </div>
                ))}
                <button type="button" onClick={addLine}>Add Line</button>

                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default OrderForm;
