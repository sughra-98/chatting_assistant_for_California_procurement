import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = {
  // Get database statistics
  getStats: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/stats`);
      return response.data;
    } catch (error) {
      console.error('Error fetching stats:', error);
      throw error;
    }
  },

  // Send a query
  sendQuery: async (question) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/query`, {
        question: question
      });
      return response.data;
    } catch (error) {
      console.error('Error sending query:', error);
      throw error;
    }
  },

  // Get departments list
  getDepartments: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/departments`);
      return response.data;
    } catch (error) {
      console.error('Error fetching departments:', error);
      throw error;
    }
  },

  // Get acquisition types
  getAcquisitionTypes: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/acquisition-types`);
      return response.data;
    } catch (error) {
      console.error('Error fetching acquisition types:', error);
      throw error;
    }
  }
};

export default api;

