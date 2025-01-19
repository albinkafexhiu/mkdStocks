import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const analysisApi = {
  getTechnicalAnalysis: async (symbol: string, timeframe: string) => {
    try {
      const response = await axios.get(
        `${API_URL}/analysis/technical/${symbol}`,
        { 
          params: { 
            timeframe,
            include_charts: true 
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error("Technical analysis request failed:", error);
      throw error;
    }
  },

  getHistoricalData: async (symbol: string, timeframe: string) => {
    try {
      const response = await axios.get(
        `${API_URL}/stocks/historical/${symbol}`,
        { 
          params: { timeframe } 
        }
      );
      return response.data;
    } catch (error) {
      console.error("Historical data request failed:", error);
      throw error;
    }
  },

  getIndicatorSettings: async () => {
    try {
      const response = await axios.get(
        `${API_URL}/analysis/indicator-settings`
      );
      return response.data;
    } catch (error) {
      console.error("Indicator settings request failed:", error);
      throw error;
    }
  },
};