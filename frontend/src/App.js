import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Orders from "./components/Orders";
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
            <p>Bienvenido, {user.username}</p>
            <button onClick={logout}>Cerrar Sesión</button>
          </div>
        )}
      </div>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/orders" element={<PrivateRoute element={<Orders />} />} />
      </Routes>
    </Router>
  );
}

export default App;
