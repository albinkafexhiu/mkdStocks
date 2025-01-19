import { useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';
import { Stock } from '../types/stock';
import toast from 'react-hot-toast';

export const useStocks = () => {
  const [popularStocks, setPopularStocks] = useState<Stock[]>([]);
  const [wishlistStocks, setWishlistStocks] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async (): Promise<void> => {
    try {
      const [popularResponse, wishlistResponse] = await Promise.all([
        axios.get<Stock[]>('http://localhost:8000/api/stocks/popular-stocks'),
        axios.get<Stock[]>('http://localhost:8000/api/stocks/wishlist')
      ]);

      setPopularStocks(popularResponse.data);
      setWishlistStocks(wishlistResponse.data);
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Failed to fetch data:', axiosError);
      toast.error('Failed to load stocks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToWishlist = async (symbol: string): Promise<void> => {
    try {
      await axios.post(`http://localhost:8000/api/stocks/wishlist/${symbol}`);
      toast.success('Added to wishlist');
      await fetchData();
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Failed to add to wishlist:', axiosError);
      toast.error('Failed to add to wishlist');
    }
  };

  const handleRemoveFromWishlist = async (symbol: string): Promise<void> => {
    try {
      await axios.delete(`http://localhost:8000/api/stocks/wishlist/${symbol}`);
      toast.success('Removed from wishlist');
      await fetchData();
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error('Failed to remove from wishlist:', axiosError);
      toast.error('Failed to remove from wishlist');
    }
  };

  const isInWishlist = (symbol: string): boolean => {
    return wishlistStocks.some(stock => stock.symbol === symbol);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return {
    popularStocks,
    wishlistStocks,
    loading,
    handleAddToWishlist,
    handleRemoveFromWishlist,
    isInWishlist,
  };
};