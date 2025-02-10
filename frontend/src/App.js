import { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import OrderList from "./components/OrderList";
import OrderForm from "./components/orders/OrderForm";
import PrivateRoute from "./components/PrivateRoute";
import { useAuth } from "./hooks/useAuth";
import { getUserProfile } from "./services/userService";

function App() {
    const { user, handleLogout } = useAuth();
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        if (user && user.email) {
            getUserProfile().then(data => {
                if (data) {
                    setUserData(data);
                }
            });
        }
    }, [user]);

    return (
        <Router>
            <div>
                {user && user.email && userData?.first_name && (
                    <div>
                        <p>Welcome, {userData.first_name}</p>
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
