import axios from 'axios';

// Create an axios instance with a base URL for our backend
const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api', // Adjust if your backend runs on a different port
});

// Use an interceptor to automatically add the JWT token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, clear it from localStorage
      localStorage.removeItem('authToken');
      // Redirect to login or refresh the page
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// --- API Functions ---
export const verifyCertificate = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/verify', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const registerInstitution = (data) => apiClient.post('/institution/register', data);
export const loginInstitution = (data) => apiClient.post('/institution/login', data);
export const addCertificate = (data) => apiClient.post('/certificate/add', data);

export const registerVerifier = (data) => apiClient.post('/verifier/register', data);
export const loginVerifier = (data) => apiClient.post('/verifier/login', data);

export default {
  verifyCertificate,
  registerInstitution,
  loginInstitution,
  addCertificate,
  registerVerifier,
  loginVerifier,
};
