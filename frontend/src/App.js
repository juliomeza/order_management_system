import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import OrderList from "./components/OrderList";
import OrderForm from "./components/OrderForm";
import PrivateRoute from "./components/PrivateRoute";
import { useAuth } from "./hooks/useAuth";

function App() {
    const { user, handleLogout } = useAuth();

    return (
        <Router>
            <div>
                {user && (
                    <div>
                        <p>Welcome, {user.first_name}</p>
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
                        user ? <Navigate to="/orders" replace /> : <Login />
                    } 
                />
                <Route path="/orders" element={<PrivateRoute element={<OrderList />} />} />
                <Route path="/create-order" element={<PrivateRoute element={<OrderForm />} />} />
            </Routes>
        </Router>
    );
}

export default App;
