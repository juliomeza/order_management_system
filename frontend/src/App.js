import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import OrderList from "./components/OrderList";
import OrderForm from "./components/OrderForm";
import { isAuthenticated, getUser, logout } from "./services/auth";
import { useState } from "react";

function PrivateRoute({ element }) {
    const auth = isAuthenticated();
    return auth ? element : <Navigate to="/" replace />;
}

function App() {
    const [user, setUser] = useState(getUser());

    const handleLogout = () => {
        logout();
        setUser(null);
    };

    return (
        <Router>
            <div>
                {user && (
                    <div>
                        <p>Welcome, {user.username}</p>
                        <button onClick={handleLogout}>
                            Logout
                        </button>
                    </div>
                )}
            </div>
            <Routes>
                <Route 
                    path="/" 
                    element={
                        isAuthenticated() ? 
                        <Navigate to="/orders" replace /> : 
                        <Login setUser={setUser} />
                    } 
                />
                <Route path="/orders" element={<PrivateRoute element={<OrderList />} />} />
                <Route path="/create-order" element={<PrivateRoute element={<OrderForm />} />} />
            </Routes>
        </Router>
    );
}

export default App;
