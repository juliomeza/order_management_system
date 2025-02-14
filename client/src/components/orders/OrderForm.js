import React from "react";
import { useOrders } from "../../hooks/useOrders";
import { useOrderFormData } from "../../hooks/useOrderFormData";
import { useNavigate } from "react-router-dom";
import OrderFormInputs from "./OrderFormInputs";
import OrderFormDropdowns from "./OrderFormDropdowns";
import OrderFormLines from "./OrderFormLines";

function OrderForm() {
    const navigate = useNavigate();
    const { addOrder } = useOrders();
    const { formData, carriers, carrierServices, warehouses, projects, materials, contacts, shippingAddresses, billingAddresses, handleChange, handleLineChange, addLine, removeLine } = useOrderFormData();

    const handleSubmit = async (e) => {
        e.preventDefault();
        addOrder(formData);
        navigate("/orders");
    };

    return (
        <div>
            <h3>Create New Order</h3>
            <form onSubmit={handleSubmit}>
                <OrderFormInputs formData={formData} handleChange={handleChange} />
                <OrderFormDropdowns 
                    formData={formData} 
                    handleChange={handleChange} 
                    carriers={carriers}
                    carrierServices={carrierServices}
                    warehouses={warehouses}
                    projects={projects}
                    contacts={contacts}
                    shippingAddresses={shippingAddresses}
                    billingAddresses={billingAddresses}
                />
                <OrderFormLines formData={formData} materials={materials} handleLineChange={handleLineChange} addLine={addLine} removeLine={removeLine} />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default OrderForm;
