import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import OrderList from "./components/OrderList";
import OrderForm from "./components/orders/OrderForm";
import PrivateRoute from "./components/PrivateRoute";
import { useAuth } from "./hooks/useAuth";

function App() {
    const { user, isLoading, handleLogout } = useAuth();

    if (isLoading) {
        return <p>Loading...</p>;  // 🔹 Mostramos un mensaje mientras se carga la sesión
    }

    return (
        <Router>
            <div>
                {user && user.email && (
                    <div>
                        <p>Welcome, {user.first_name || "User"}</p>
                        <button onClick={handleLogout}>Logout</button>
                    </div>
                )}
            </div>
            <Routes>
                <Route 
                    path="/" 
                    element={
                        user && user.email ? <Navigate to="/orders" replace /> : <Login />
                    } 
                />
                <Route path="/orders" element={<PrivateRoute element={<OrderList />} />} />
                <Route path="/create-order" element={<PrivateRoute element={<OrderForm />} />} />
            </Routes>
        </Router>
    );
}

export default App;
