import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { StockData } from '../../types/stockdata';

interface StockChartProps {
  data: StockData[];
}

export const StockChart: React.FC<StockChartProps> = ({ data }) => (
  <div className="h-[400px]">
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <XAxis 
          dataKey="date" 
          tick={{ fontSize: 12 }}
          interval="preserveStartEnd"
        />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />
        <Legend />
        <Line 
          type="monotone" 
          dataKey="lastTradePrice" 
          name="Last Trade Price"
          stroke="#2563eb" 
          strokeWidth={2} 
          dot={false}
        />
        <Line 
          type="monotone" 
          dataKey="maxPrice" 
          name="Max Price"
          stroke="#16a34a" 
          strokeWidth={2} 
          dot={false}
        />
        <Line 
          type="monotone" 
          dataKey="minPrice" 
          name="Min Price"
          stroke="#dc2626" 
          strokeWidth={2} 
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  </div>
);