import React from "react";

function OrderFormLines({ formData, materials, handleLineChange, addLine, removeLine }) {
    return (
        <div>
            <h4>Order Lines</h4>
            {formData.lines.map((line, index) => (
                <div key={index}>
                    <select name="material" value={line.material} onChange={(e) => handleLineChange(index, e)} required>
                        <option value="">Select Material</option>
                        {materials.map(material => <option key={material.id} value={material.material}>{material.material_name}</option>)}
                    </select>
                    <input type="number" name="quantity" placeholder="Quantity" value={line.quantity} onChange={(e) => handleLineChange(index, e)} required />
                    <button type="button" onClick={() => removeLine(index)}>Delete</button>
                </div>
            ))}
            <button type="button" onClick={addLine}>Add Line</button>
        </div>
    );
}

export default OrderFormLines;
