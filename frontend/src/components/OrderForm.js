import React, { useState, useEffect } from "react";
import { createOrder } from "../services/orderService";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function OrderForm() {
    const navigate = useNavigate();
    const [carriers, setCarriers] = useState([]);
    const [carrierServices, setCarrierServices] = useState([]);
    const [warehouses, setWarehouses] = useState([]);
    const [projects, setProjects] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [contacts, setContacts] = useState([]);
    const [shippingAddresses, setShippingAddresses] = useState([]);
    const [billingAddresses, setBillingAddresses] = useState([]);

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

    /* Fetch Project Warehouse Carrier and CarrierService from API */
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

    /* Fetch Inventory from API */
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

    /* Fetch Contacts from API */
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
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    
        // Si el usuario cambia el contacto, actualizamos las direcciones
        if (name === "contact") {
            // Buscar el contacto seleccionado en la lista
            const selectedContact = contacts.find(contact => contact.id.toString() === value);
            
            if (selectedContact) {
                // Filtrar las direcciones según su tipo
                const shipping = selectedContact.addresses.filter(addr => addr.address_type === "shipping");
                const billing = selectedContact.addresses.filter(addr => addr.address_type === "billing");
    
                setShippingAddresses(shipping);
                setBillingAddresses(billing);
    
                // Autoseleccionar la primera dirección disponible de cada tipo
                setFormData((prevData) => ({
                    ...prevData,
                    shipping_address: shipping.length > 0 ? shipping[0].id : "",
                    billing_address: billing.length > 0 ? billing[0].id : ""
                }));
            } else {
                // Si el contacto no tiene direcciones, limpiar los dropdowns
                setShippingAddresses([]);
                setBillingAddresses([]);
                setFormData((prevData) => ({
                    ...prevData,
                    shipping_address: "",
                    billing_address: ""
                }));
            }
        }
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

                {/* Dropdown para Shipping Address */}
                <select name="shipping_address" value={formData.shipping_address} onChange={handleChange} required>
                    <option value="">Select Shipping Address</option>
                    {shippingAddresses.map(address => (
                        <option key={address.id} value={address.id}>
                            {address.address_line_1}, {address.city}, {address.state}, {address.country}
                        </option>
                    ))}
                </select>

                {/* Dropdown para Billing Address */}
                <select name="billing_address" value={formData.billing_address} onChange={handleChange} required>
                    <option value="">Select Billing Address</option>
                    {billingAddresses.map(address => (
                        <option key={address.id} value={address.id}>
                            {address.address_line_1}, {address.city}, {address.state}, {address.country}
                        </option>
                    ))}
                </select>

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
