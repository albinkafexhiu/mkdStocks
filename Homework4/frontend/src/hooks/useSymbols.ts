// src/hooks/useSymbols.ts
import { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const API_URL = import.meta.env.VITE_API_URL;

export const useSymbols = (initialSymbol?: string) => {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState(initialSymbol || '');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSymbols = async () => {
      try {
        const response = await axios.get(`${API_URL}/stocks/symbols`);
        setSymbols(response.data);
      } catch (error) {
        toast.error('Failed to fetch stock symbols');
        console.error("Analysis error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSymbols();
  }, []);

  // Update selected symbol if initialSymbol changes
  useEffect(() => {
    if (initialSymbol) {
      setSelectedSymbol(initialSymbol);
    }
  }, [initialSymbol]);

  return {
    symbols,
    selectedSymbol,
    setSelectedSymbol,
    loading
  };
};