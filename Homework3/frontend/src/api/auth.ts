import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const authApi = {
  register: async (userData: { email: string; password: string; full_name: string }) => {
    const response = await axios.post(`${API_URL}/auth/register`, userData);
    return response.data;
  },

  login: async (credentials: { email: string; password: string }) => {
    const response = await axios.post(`${API_URL}/auth/login`, credentials);
    return response.data;
  }
};