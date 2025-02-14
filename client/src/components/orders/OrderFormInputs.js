import React from "react";

function OrderFormInputs({ formData, handleChange }) {
    return (
        <>
            <input type="text" name="lookup_code_order" placeholder="Order Number" value={formData.lookup_code_order} onChange={handleChange} required />
            <input type="text" name="lookup_code_shipment" placeholder="Shipment Number" value={formData.lookup_code_shipment} onChange={handleChange} required />
            <input type="date" name="expected_delivery_date" value={formData.expected_delivery_date} onChange={handleChange} required />
        </>
    );
}

export default OrderFormInputs;
