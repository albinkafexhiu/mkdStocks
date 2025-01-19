import React from 'react';
import { TrendingUp, TrendingDown, BarChart2, DollarSign } from 'lucide-react';
import { StatCard } from '../components/dashboard/StatCard';
import { StockTable } from '../components/dashboard/StockTable';
import { VolumeChart } from '../components/dashboard/VolumeChart';
import { useMarketData } from '../hooks/useMarketData';
import { formatCurrency } from '../utils/formatters';

const DashboardPage: React.FC = () => {
  const { marketStats, topGainers, topLosers, volumeLeaders, loading } = useMarketData();

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

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Gainers"
          value={marketStats.gainers}
          Icon={TrendingUp}
          colorClass="bg-green-100 text-green-600"
        />
        <StatCard
          title="Losers"
          value={marketStats.losers}
          Icon={TrendingDown}
          colorClass="bg-red-100 text-red-600"
        />
        <StatCard
          title="Total Volume"
          value={marketStats.totalVolume.toLocaleString()}
          Icon={BarChart2}
          colorClass="bg-blue-100 text-blue-600"
        />
        <StatCard
          title="Total Turnover"
          value={formatCurrency(marketStats.totalTurnover)}
          Icon={DollarSign}
          colorClass="bg-purple-100 text-purple-600"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <StockTable title="Top Gainers" data={topGainers} type="gainers" />
        <StockTable title="Top Losers" data={topLosers} type="losers" />
      </div>

      <VolumeChart data={volumeLeaders} />
    </div>
  );
};

export default DashboardPage;