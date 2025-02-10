import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import OrderList from "./components/OrderList";
import OrderForm from "./components/orders/OrderForm";
import PrivateRoute from "./components/PrivateRoute";
import { useAuth } from "./hooks/useAuth";

function App() {
    const { user, handleLogout } = useAuth();

    return (
        <Router>
            <div>
            {user && user.email && (
                <div>
                    <p>Welcome, {user.email}</p>
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
