import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

const chatbotService = {
  sendMessage: async (message) => {
    try {
      const response = await axios.post(`${API_URL}/chatbot/message`, { message });
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  getConversationHistory: async () => {
    try {
      const response = await axios.get(`${API_URL}/chatbot/history`);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },
};

export default chatbotService;