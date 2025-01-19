import { useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';
import { MarketData, MarketStats } from '../types/market';

export const useMarketData = () => {
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMarketData = async () => {
      try {
        const response = await axios.get<MarketData[]>('http://localhost:8000/api/stocks/market-overview');
        setMarketData(response.data);
      } catch (error) {
        const axiosError = error as AxiosError;
        console.error('Failed to fetch market data:', axiosError);
      } finally {
        setLoading(false);
      }
    };

    fetchMarketData();
  }, []);

  const marketStats: MarketStats = {
    totalTurnover: marketData.reduce((sum, stock) => sum + stock.totalTurnover, 0),
    totalVolume: marketData.reduce((sum, stock) => sum + stock.totalVolume, 0),
    gainers: marketData.filter(stock => stock.priceChange > 0).length,
    losers: marketData.filter(stock => stock.priceChange < 0).length
  };

  const topGainers = [...marketData]
    .filter(stock => stock.priceChange > 0)
    .sort((a, b) => b.priceChange - a.priceChange)
    .slice(0, 5);

  const topLosers = [...marketData]
    .filter(stock => stock.priceChange < 0)
    .sort((a, b) => a.priceChange - b.priceChange)
    .slice(0, 5);

  const volumeLeaders = [...marketData]
    .sort((a, b) => b.totalVolume - a.totalVolume)
    .slice(0, 10);

  return {
    marketData,
    marketStats,
    topGainers,
    topLosers,
    volumeLeaders,
    loading
  };
};