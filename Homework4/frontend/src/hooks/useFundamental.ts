import { useState, useEffect } from 'react';
import { useSymbols } from './useSymbols';
import { fundamentalApi } from '../api/fundamental';
import { NewsData, MarketSentiment } from '../types/fundamental';
import toast from 'react-hot-toast';

export const useFundamental = () => {
  const { symbols, selectedSymbol, setSelectedSymbol, loading: symbolsLoading } = useSymbols();
  const [newsData, setNewsData] = useState<NewsData | null>(null);
  const [marketSentiment, setMarketSentiment] = useState<MarketSentiment | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMarketSentiment();
  }, []);

  const fetchMarketSentiment = async () => {
    try {
      const data = await fundamentalApi.getMarketSentiment();
      setMarketSentiment(data);
    } catch (err) {
      console.error('Failed to fetch market sentiment:', err);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedSymbol) {
      toast.error('Please select a symbol');
      return;
    }

    setLoading(true);
    try {
      const [newsResponse, sentimentResponse] = await Promise.all([
        fundamentalApi.getLatestNews(selectedSymbol),
        fundamentalApi.getSentiment(selectedSymbol)
      ]);
      
      setNewsData({
        ...newsResponse,
        sentiment: sentimentResponse
      });
    } catch (err) {
      toast.error('Failed to fetch analysis');
      console.error("Analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  return {
    symbols,
    selectedSymbol,
    setSelectedSymbol,
    newsData,
    marketSentiment,
    loading,
    symbolsLoading,
    handleAnalyze
  };
};