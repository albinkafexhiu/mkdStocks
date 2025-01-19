import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { MarketData } from '../../types/market';

interface VolumeChartProps {
  data: MarketData[];
}

export const VolumeChart: React.FC<VolumeChartProps> = ({ data }) => (
  <div className="bg-white rounded-lg shadow-md">
    <div className="p-6 border-b border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900">Volume Leaders</h2>
    </div>
    <div className="p-6">
      <div className="h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
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
);