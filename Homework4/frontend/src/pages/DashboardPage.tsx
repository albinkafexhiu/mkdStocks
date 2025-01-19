import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { BarChart2, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

// Define TypeScript interfaces
interface StockData {
  symbol: string;
  currentPrice: number;
  startPrice: number;
  priceChange: number;
  totalVolume: number;
  totalTurnover: number;
  lastTradeDate: string;
}

interface MarketStats {
  totalTurnover: number;
  totalVolume: number;
  gainers: number;
  losers: number;
}

const DashboardPage = () => {
  const [marketData, setMarketData] = useState<StockData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMarketData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/stocks/market-overview');
        setMarketData(response.data);
      } catch (error) {
        console.error('Failed to fetch market data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMarketData();
  }, []);

  // Calculate market statistics
  const marketStats: MarketStats = {
    totalTurnover: marketData.reduce((sum, stock) => sum + stock.totalTurnover, 0),
    totalVolume: marketData.reduce((sum, stock) => sum + stock.totalVolume, 0),
    gainers: marketData.filter(stock => stock.priceChange > 0).length,
    losers: marketData.filter(stock => stock.priceChange < 0).length
  };

  // Sort data for different categories
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

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'MKD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-gray-600">Loading market data...</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Market Overview</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Gainers Card */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Gainers</p>
              <p className="text-2xl font-semibold text-gray-900">{marketStats.gainers}</p>
            </div>
          </div>
        </div>

        {/* Losers Card */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <TrendingDown className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Losers</p>
              <p className="text-2xl font-semibold text-gray-900">{marketStats.losers}</p>
            </div>
          </div>
        </div>

        {/* Volume Card */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BarChart2 className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Volume</p>
              <p className="text-2xl font-semibold text-gray-900">
                {marketStats.totalVolume.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        {/* Turnover Card */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Turnover</p>
              <p className="text-2xl font-semibold text-gray-900">
                {formatCurrency(marketStats.totalTurnover)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Top Gainers & Losers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Gainers Table */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Top Gainers</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Symbol</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">Price</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">Change</th>
                </tr>
              </thead>
              <tbody>
                {topGainers.map((stock) => (
                  <tr key={stock.symbol} className="border-t border-gray-200">
                    <td className="py-3 px-4">{stock.symbol}</td>
                    <td className="text-right py-3 px-4">{formatCurrency(stock.currentPrice)}</td>
                    <td className="text-right py-3 px-4 text-green-600">
                      +{stock.priceChange.toFixed(2)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Losers Table */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Top Losers</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Symbol</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">Price</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">Change</th>
                </tr>
              </thead>
              <tbody>
                {topLosers.map((stock) => (
                  <tr key={stock.symbol} className="border-t border-gray-200">
                    <td className="py-3 px-4">{stock.symbol}</td>
                    <td className="text-right py-3 px-4">{formatCurrency(stock.currentPrice)}</td>
                    <td className="text-right py-3 px-4 text-red-600">
                      {stock.priceChange.toFixed(2)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Volume Leaders Chart */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Volume Leaders</h2>
        </div>
        <div className="p-6">
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={volumeLeaders}>
                <XAxis dataKey="symbol" />
                <YAxis />
                <Tooltip 
                  formatter={(value: number) => [value.toLocaleString(), 'Volume']}
                  labelFormatter={(label: string) => `Symbol: ${label}`}
                />
                <Bar 
                  dataKey="totalVolume" 
                  fill="#3B82F6"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;