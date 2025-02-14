import { useState, useEffect } from "react";
import API from "../services/api";

export function useOrderFormData() {
    const [formData, setFormData] = useState({
        lookup_code_order: "",
        lookup_code_shipment: "",
        status: "3", // Created
        order_type: "2", // Outbound
        order_class: "1", // Sales Orders
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

    const [carriers, setCarriers] = useState([]);
    const [carrierServices, setCarrierServices] = useState([]);
    const [warehouses, setWarehouses] = useState([]);
    const [projects, setProjects] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [contacts, setContacts] = useState([]);
    const [shippingAddresses, setShippingAddresses] = useState([]);
    const [billingAddresses, setBillingAddresses] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = sessionStorage.getItem("token");
                if (!token) {
                    console.error("No access token found, redirecting to login.");
                    window.location.href = "/";
                    return;
                }

                const headers = { Authorization: `Bearer ${token}` };

                const [carriersRes, servicesRes, warehousesRes, projectsRes, materialsRes, contactsRes] = await Promise.all([
                    API.get("/carriers/", { headers }),
                    API.get("/carrier-services/", { headers }),
                    API.get("/warehouses/", { headers }),
                    API.get("/projects/", { headers }),
                    API.get("/inventory/list/", { headers }),
                    API.get("/contacts/list/", { headers })
                ]);

                setCarriers(carriersRes.data);
                setCarrierServices(servicesRes.data);
                setWarehouses(warehousesRes.data);
                setProjects(projectsRes.data);
                setMaterials(materialsRes.data.results || materialsRes.data);
                setContacts(contactsRes.data.results || []);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));

        if (name === "contact") {
            const selectedContact = contacts.find(contact => contact.id.toString() === value);
            if (selectedContact) {
                const shipping = selectedContact.addresses.filter(addr => addr.address_type === "shipping");
                const billing = selectedContact.addresses.filter(addr => addr.address_type === "billing");

                setShippingAddresses(shipping);
                setBillingAddresses(billing);

                setFormData((prevData) => ({
                    ...prevData,
                    shipping_address: shipping.length > 0 ? shipping[0].id : "",
                    billing_address: billing.length > 0 ? billing[0].id : ""
                }));
            } else {
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
        setFormData((prevData) => {
            const newLines = [...prevData.lines];
            newLines[index][name] = value;
            return { ...prevData, lines: newLines };
        });
    };

    const addLine = () => {
        setFormData((prevData) => ({
            ...prevData,
            lines: [...prevData.lines, { material: "", quantity: "" }]
        }));
    };

    const removeLine = (index) => {
        setFormData((prevData) => ({
            ...prevData,
            lines: prevData.lines.filter((_, i) => i !== index)
        }));
    };

    return {
        formData,
        setFormData,
        carriers,
        carrierServices,
        warehouses,
        projects,
        materials,
        contacts,
        shippingAddresses,
        billingAddresses,
        handleChange,
        handleLineChange,
        addLine,
        removeLine
    };
}
