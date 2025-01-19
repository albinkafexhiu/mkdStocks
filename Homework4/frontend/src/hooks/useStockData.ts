import { useState } from 'react';  
import axios from 'axios';
import { StockData } from '../types/stockdata';  
import toast from 'react-hot-toast';


export const useStockData = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [stockData, setStockData] = useState<StockData[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchStockData = async (symbol: string) => { 
    if (!symbol) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/stocks/data/${symbol}`, {
        params: { 
          start_date: startDate,  
          end_date: endDate 
        }
      });
      setStockData(response.data);
      toast.success('Data loaded successfully');
    } catch (error) {
      toast.error('Failed to fetch stock data');
      console.error('Stock data fetch error:', error);  
    } finally {
      setLoading(false);
    }
  };

  const handleTimeRangeSelect = (days: number) => {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);
    
    const startStr = start.toISOString().split('T')[0];
    const endStr = end.toISOString().split('T')[0];
    
    setStartDate(startStr);
    setEndDate(endStr);
  };

  return {
    startDate,
    setStartDate,
    endDate,
    setEndDate,
    stockData,
    loading,
    fetchStockData,
    handleTimeRangeSelect
  };
};