import React, { useState, useEffect } from "react";
import { createOrder } from "../services/orders";
import { useNavigate } from "react-router-dom";
import API from "../api";

function OrderForm() {
    const navigate = useNavigate();
    const [carriers, setCarriers] = useState([]);
    const [carrierServices, setCarrierServices] = useState([]);
    const [warehouses, setWarehouses] = useState([]);
    const [projects, setProjects] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [contacts, setContacts] = useState([]);

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

    {/* Fetch Project Warehouse Carrier and CarrierService from API */}
    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            if (!token) {
                console.error("No access token found, redirecting to login.");
                window.location.href = "/";
                return;
            }

            try {
                const headers = { Authorization: `Bearer ${token}` };

                const [carriersRes, servicesRes, warehousesRes, projectsRes] = await Promise.all([
                    API.get("/carriers/", { headers }),
                    API.get("/carrier-services/", { headers }),
                    API.get("/warehouses/", { headers }),
                    API.get("/projects/", { headers })
                ]);

                setCarriers(carriersRes.data);
                setCarrierServices(servicesRes.data);
                setWarehouses(warehousesRes.data);
                setProjects(projectsRes.data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, []);

    {/* Fetch Inventory from API */}
    useEffect(() => {
        const fetchMaterials = async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    console.error("No access token found, redirecting to login.");
                    window.location.href = "/";
                    return;
                }
    
                const response = await API.get("/inventory/list/", {
                    headers: { Authorization: `Bearer ${token}` },
                });
    
                setMaterials(response.data.results || response.data); // Maneja paginación si `results` es usado
            } catch (error) {
                console.error("Error fetching materials:", error);
            }
        };
    
        fetchMaterials();
    }, []);

    {/* Fetch Contacts from API */}
    useEffect(() => {
        const fetchContacts = async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    console.error("No access token found, redirecting to login.");
                    window.location.href = "/";
                    return;
                }
    
                const response = await API.get("/contacts/list/", {
                    headers: { Authorization: `Bearer ${token}` },
                });
    
                setContacts(response.data.results || []);
            } catch (error) {
                console.error("Error fetching contacts:", error);
            }
        };
    
        fetchContacts();
    }, []);    

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleLineChange = (index, e) => {
        const { name, value } = e.target;
        const newLines = [...formData.lines];
    
        newLines[index][name] = value;

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

                {/* Dropdown para Project */}
                <select name="project" value={formData.project} onChange={handleChange} required>
                    <option value="">Select Project</option>
                    {projects.map(project => (
                        <option key={project.id} value={project.id}>{project.name}</option>
                    ))}
                </select>

                {/* Dropdown para Warehouse */}
                <select name="warehouse" value={formData.warehouse} onChange={handleChange} required>
                    <option value="">Select Warehouse</option>
                    {warehouses.map(warehouse => (
                        <option key={warehouse.id} value={warehouse.id}>{warehouse.name}</option>
                    ))}
                </select>

                {/* Dropdown para Contact */}
                <select name="contact" value={formData.contact} onChange={handleChange} required>
                    <option value="">Select Contact</option>
                    {contacts.map(contact => (
                        <option key={contact.id} value={contact.id}>
                            {contact.first_name} {contact.last_name}
                        </option>
                    ))}
                </select>

                <input type="number" name="shipping_address" placeholder="Shipping Address" value={formData.shipping_address} onChange={handleChange} required />
                <input type="number" name="billing_address" placeholder="Billing Address" value={formData.billing_address} onChange={handleChange} required />

                {/* Dropdown para Carrier */}
                <select name="carrier" value={formData.carrier} onChange={handleChange}>
                    <option value="">Select Carrier</option>
                    {carriers.map(carrier => (
                        <option key={carrier.id} value={carrier.id}>{carrier.name}</option>
                    ))}
                </select>

                {/* Dropdown para Carrier Service */}
                <select name="service_type" value={formData.service_type} onChange={handleChange}>
                    <option value="">Select Carrier Service</option>
                    {carrierServices.map(service => (
                        <option key={service.id} value={service.id}>{service.name}</option>
                    ))}
                </select>

                <input type="date" name="expected_delivery_date" placeholder="Expected Delivery Date" value={formData.expected_delivery_date} onChange={handleChange} />
                <textarea name="notes" placeholder="Notes" value={formData.notes} onChange={handleChange}></textarea>

                <h4>Order Lines</h4>
                {formData.lines.map((line, index) => (
                    <div key={index}>
                        {/* Dropdown para Material */}
                        <select name="material" value={line.material} onChange={(e) => handleLineChange(index, e)} required>
                            <option value="">Select Material</option>
                            {materials.map(material => (
                                <option key={material.id} value={material.material}>{material.material_name}</option>
                            ))}
                        </select>

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
