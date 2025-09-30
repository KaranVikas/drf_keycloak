import keycloak from '../keycloak';
import apiClient from './api';

export const userService = {

  getMe: async () => {
    const token = keycloak.token; // or however you get the token
    console.log('Sending request with apiService...');

    console.log('Sending request with token:', token ? 'Token present' : 'No token');
    console.log("token", token)
    const response = await apiClient.get('/users/me/',{
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },
};