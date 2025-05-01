import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const instance = axios.create({
  baseURL,
  withCredentials: false, // Set to true only if cookies are used
  timeout: 10000, // 10-second timeout
});

// Request interceptor: Add Bearer token
instance.interceptors.request.use((config) => {
  if (import.meta.env.DEV) {
    console.log('API Request:', config.method.toUpperCase(), config.url);
  }
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor: Handle 401 and token refresh
instance.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log('API Response:', response.status, response.data);
    }
    return response;
  },
  async (error) => {
    if (import.meta.env.DEV) {
      console.error('API Error:', error.response?.status, error.message);
    }

    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const { data } = await axios.post(`${baseURL}/api/users/auth/token/refresh/`, {
          refresh: localStorage.getItem('refresh_token'),
        });
        console.log("refreshed token", data)
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return instance(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth';
        return Promise.reject(refreshError);
      }
    }

    if (!error.response) {
      console.error('Network error: Please check your internet connection');
      // Optionally notify user
    }

    return Promise.reject(error);
  }
);

export default instance;