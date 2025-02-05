import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import OrderList from "./components/OrderList";
import OrderForm from "./components/OrderForm";
import { isAuthenticated, getUser, logout } from "./services/auth";

function PrivateRoute({ element }) {
  return isAuthenticated() ? element : <Navigate to="/" />;
}

function App() {
  const user = getUser();

  return (
    <Router>
      <div>
        {user && (
          <div>
            <p>Welcome, {user.username}</p>
            <button onClick={logout}>Logout</button>
          </div>
        )}
      </div>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/orders" element={<PrivateRoute element={<OrderList />} />} />
        <Route path="/create-order" element={<PrivateRoute element={<OrderForm />} />} />
      </Routes>
    </Router>
  );
}

export default App;
