import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { MarketSentiment } from '../../types/fundamental';

interface MarketOverviewProps {
  data: MarketSentiment;
}

const COLORS = ['#4ade80', '#facc15', '#ef4444'];

export const MarketOverview: React.FC<MarketOverviewProps> = ({ data }) => {
  if (!data) return null;

  const pieData = [
    { name: 'Buy', value: data.recommendations.buy },
    { name: 'Hold', value: data.recommendations.hold },
    { name: 'Sell', value: data.recommendations.sell }
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <h2 className="text-xl font-semibold mb-4">Market Sentiment Overview</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="h-64">
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label
              >
                {pieData.map((_entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex flex-col justify-center">
          <p className="text-sm text-gray-600">Average Market Sentiment</p>
          <p className="text-2xl font-bold">{(data.market_sentiment * 100).toFixed(1)}%</p>
          <p className="text-sm text-gray-600 mt-4">Companies Analyzed</p>
          <p className="text-xl">{data.total_companies_analyzed}</p>
          <p className="text-sm text-gray-500 mt-2">Last Updated: {data.analysis_date}</p>
        </div>
      </div>
    </div>
  );
};