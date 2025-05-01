// AuthProvider.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import instance from '../api/axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      get_user().finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const get_user = async () => {
    try {
      const { data } = await instance.get('/api/users/me/');
      setUser(data);
    } catch (err) {
      console.error('Failed to fetch user:', err);
      if (err.response?.status === 401) {
        localStorage.removeItem('access_token'); // Clear invalid token
        // Optionally redirect to login or show a message
      }
      setUser(null);
    }
  };

  const login = async (email, password) => {
    setLoading(true);
    try {
      const { data } = await instance.post('/api/users/auth/token/', { email, password });
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh); // Store refresh token
      await get_user();
    } finally {
      setLoading(false);
    }
  };

  const signup = async (payload) => {
    const { data } = await instance.post('/auth/signup', payload);
    localStorage.setItem('access_token', data.token);
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);