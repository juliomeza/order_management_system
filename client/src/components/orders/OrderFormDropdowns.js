import React from "react";

function OrderFormDropdowns({ formData, handleChange, carriers, carrierServices, warehouses, projects, contacts, shippingAddresses, billingAddresses }) {
    return (
        <>
            <select name="project" value={formData.project} onChange={handleChange} required>
                <option value="">Select Project</option>
                {projects.map(project => <option key={project.id} value={project.id}>{project.name}</option>)}
            </select>

            <select name="warehouse" value={formData.warehouse} onChange={handleChange} required>
                <option value="">Select Warehouse</option>
                {warehouses.map(warehouse => <option key={warehouse.id} value={warehouse.id}>{warehouse.name}</option>)}
            </select>

            <select name="contact" value={formData.contact} onChange={handleChange} required>
                <option value="">Select Contact</option>
                {contacts.map(contact => <option key={contact.id} value={contact.id}>{contact.first_name} {contact.last_name}</option>)}
            </select>

            <select name="shipping_address" value={formData.shipping_address} onChange={handleChange} required>
                <option value="">Select Shipping Address</option>
                {shippingAddresses.map(address => <option key={address.id} value={address.id}>{address.address_line_1}</option>)}
            </select>

            <select name="billing_address" value={formData.billing_address} onChange={handleChange} required>
                <option value="">Select Billing Address</option>
                {billingAddresses.map(address => <option key={address.id} value={address.id}>{address.address_line_1}</option>)}
            </select>

            {/* 🚀 Se agregaron los dropdowns de Carrier y Carrier Service */}
            <select name="carrier" value={formData.carrier} onChange={handleChange}>
                <option value="">Select Carrier</option>
                {carriers.map(carrier => (
                    <option key={carrier.id} value={carrier.id}>{carrier.name}</option>
                ))}
            </select>

            <select name="service_type" value={formData.service_type} onChange={handleChange}>
                <option value="">Select Carrier Service</option>
                {carrierServices.map(service => (
                    <option key={service.id} value={service.id}>{service.name}</option>
                ))}
            </select>
        </>
    );
}

export default OrderFormDropdowns;
