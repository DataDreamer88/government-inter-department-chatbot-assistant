// frontend/src/services/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
const API_TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT) || 30000;

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to connect to server');
    }
  },

  // Send query
  sendQuery: async (query) => {
    try {
      const response = await apiClient.post('/api/query', { query });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to process query');
    }
  },

  // Get statistics
  getStats: async () => {
    try {
      const response = await apiClient.get('/api/stats');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get statistics');
    }
  },

  // Search datasets
  searchDatasets: async (query) => {
    try {
      const response = await apiClient.post('/api/search_datasets', { query });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to search datasets');
    }
  },

  // Trigger indexing
  indexData: async () => {
    try {
      const response = await apiClient.post('/api/index');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to index data');
    }
  },
};

export default api;