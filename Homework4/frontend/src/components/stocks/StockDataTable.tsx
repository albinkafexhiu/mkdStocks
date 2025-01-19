import React from 'react';
import { StockData } from '../../types/stockdata';

interface StockDataTableProps {
  data: StockData[];
}

export const StockDataTable: React.FC<StockDataTableProps> = ({ data }) => (
  <div className="overflow-x-auto" style={{ maxHeight: '400px' }}>
    <table className="min-w-full divide-y divide-gray-200">
      <thead className="bg-gray-50 sticky top-0">
        <tr>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Price</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max Price</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Min Price</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Change %</th>
          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
        </tr>
      </thead>
      <tbody className="bg-white divide-y divide-gray-200">
        {data.map((row, index) => (
          <tr key={index} className="hover:bg-gray-50">
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{row.date}</td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{row.lastTradePrice.toFixed(2)}</td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{row.maxPrice.toFixed(2)}</td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{row.minPrice.toFixed(2)}</td>
            <td className={`px-6 py-4 whitespace-nowrap text-sm ${row.changePercentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {row.changePercentage.toFixed(2)}%
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{row.volume.toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);