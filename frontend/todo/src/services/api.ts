import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('keycloak-token');
  if(token){
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default apiClient