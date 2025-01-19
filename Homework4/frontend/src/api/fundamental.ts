import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fundamentalApi = {
  // Get all news and sentiment data for a company
  getCompanyNews: async (symbol: string) => {
    try {
      const response = await axios.get(`${API_URL}/fundamental/news/${symbol}`);
      return response.data;
    } catch (error) {
      console.error('News analysis request failed:', error);
      throw error;
    }
  },

  // Get latest news only
  getLatestNews: async (symbol: string, limit: number = 5) => {
    try {
      const response = await axios.get(`${API_URL}/fundamental/news/${symbol}/latest`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Latest news request failed:', error);
      throw error;
    }
  },

  // Get sentiment analysis only
  getSentiment: async (symbol: string) => {
    try {
      const response = await axios.get(`${API_URL}/fundamental/news/${symbol}/sentiment`);
      return response.data;
    } catch (error) {
      console.error('Sentiment analysis request failed:', error);
      throw error;
    }
  },

  // Get market-wide sentiment
  getMarketSentiment: async () => {
    try {
      const response = await axios.get(`${API_URL}/fundamental/market/sentiment`);
      return response.data;
    } catch (error) {
      console.error('Market sentiment request failed:', error);
      throw error;
    }
  }
};