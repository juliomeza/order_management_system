import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function PrivateRoute({ element }) {
    const { user, isLoading } = useAuth();

    if (isLoading) {
        return <p>Loading...</p>;
    }

    return user ? element : <Navigate to="/" replace />;
}

export default PrivateRoute;
