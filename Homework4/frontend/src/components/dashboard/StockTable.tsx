import React from 'react';
import { MarketData } from '../../types/market';
import { formatCurrency } from '../../utils/formatters';

interface StockTableProps {
  title: string;
  data: MarketData[];
  type: 'gainers' | 'losers';
}

export const StockTable: React.FC<StockTableProps> = ({ title, data, type }) => (
  <div className="bg-white rounded-lg shadow-md">
    <div className="p-6 border-b border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
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
          {data.map((stock) => (
            <tr key={stock.symbol} className="border-t border-gray-200">
              <td className="py-3 px-4">{stock.symbol}</td>
              <td className="text-right py-3 px-4">{formatCurrency(stock.currentPrice)}</td>
              <td className={`text-right py-3 px-4 ${type === 'gainers' ? 'text-green-600' : 'text-red-600'}`}>
                {type === 'gainers' ? '+' : ''}{stock.priceChange.toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);