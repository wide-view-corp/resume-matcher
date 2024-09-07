import axios from 'axios';

const API_URL = 'http://localhost:3300'; // Adjust this URL as needed

const datasetService = {
  getDocuments: async () => {
    try {
      const response = await axios.get(`${API_URL}/resumes`);
      return response.data;
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  },

  uploadDocument: async (formData) => {
    try {
      const response = await axios.post(`${API_URL}/resumes`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading document:', error.response ? error.response.data : error.message);
      throw error;
    }
  },

  deleteDocument: async (id) => {
    try {
      await axios.delete(`${API_URL}/resumes/${id}`);
    } catch (error) {
      console.error('Error deleting document:', error);
      throw error;
    }
  },

  getDocumentContent: async (id) => {
    try {
      const response = await axios.get(`${API_URL}/resumes/${id}/content`, {
        responseType: 'blob',
      });
      return URL.createObjectURL(response.data);
    } catch (error) {
      console.error('Error fetching document content:', error);
      throw error;
    }
  },
};

export default datasetService;