import { useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';
import { SearchStock } from '../types/stock';

export const useStockSearch = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [searchResults, setSearchResults] = useState<SearchStock[]>([]);
  const [showSearchResults, setShowSearchResults] = useState<boolean>(false);

  const handleSearch = async (): Promise<void> => {
    try {
      const response = await axios.get<string[]>('http://localhost:8000/api/stocks/symbols');
      const filteredStocks = response.data.filter((symbol) =>
        symbol.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setSearchResults(filteredStocks.map(symbol => ({ symbol })));
      setShowSearchResults(true);
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Search failed:', axiosError);
    }
  };

  useEffect(() => {
    if (searchQuery) {
      handleSearch();
    } else {
      setSearchResults([]);
      setShowSearchResults(false);
    }
  }, [searchQuery]);

  return {
    searchQuery,
    setSearchQuery,
    searchResults,
    showSearchResults,
  };
};