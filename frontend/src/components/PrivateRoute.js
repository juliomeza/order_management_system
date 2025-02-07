import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";

function PrivateRoute({ element }) {
    return isAuthenticated() ? element : <Navigate to="/" replace />;
}

export default PrivateRoute;
