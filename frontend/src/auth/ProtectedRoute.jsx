// ProtectedRoute.jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthProvider';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  console.log('User:by ProtectedRoute', user);

  if (loading) return <div>Loading...</div>;

  return user ? children : <Navigate to="/auth" />;
}
