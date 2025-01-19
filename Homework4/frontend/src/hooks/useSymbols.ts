// src/hooks/useSymbols.ts
import { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

export const useSymbols = (initialSymbol?: string) => {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState(initialSymbol || '');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSymbols = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/stocks/symbols');
        setSymbols(response.data);
      } catch (error) {
        toast.error('Failed to fetch stock symbols');
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