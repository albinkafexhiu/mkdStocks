import React from 'react';
import { Star } from 'lucide-react';
import { Stock } from '../../types/stock';
import { formatCurrency } from '../../utils/formatters';

interface StockCardProps {
  stock: Stock;
  isInWishlist: boolean;
  onWishlistToggle: (symbol: string) => Promise<void>;
  onClick: () => void;
}

export const StockCard: React.FC<StockCardProps> = ({
  stock,
  isInWishlist,
  onWishlistToggle,
  onClick,
}) => (
  <div
    className="bg-white rounded-lg shadow-md p-6 cursor-pointer"
    onClick={onClick}
  >
    <div className="flex justify-between items-start mb-4">
      <div>
        <h3 className="text-lg font-semibold text-gray-900">
          {stock.companyName || stock.symbol}
        </h3>
        <p className="text-sm text-gray-500">{stock.symbol}</p>
      </div>
      <button
        onClick={(e) => {
          e.stopPropagation();
          onWishlistToggle(stock.symbol);
        }}
        className="p-2 hover:bg-gray-100 rounded-full"
      >
        <Star
          className={`h-5 w-5 ${
            isInWishlist ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400'
          }`}
        />
      </button>
    </div>
    <div className="flex justify-between items-baseline">
      <span className="text-xl font-semibold">
        {formatCurrency(stock.price)}
      </span>
      <span
        className={`font-medium ${
          stock.changePercentage > 0
            ? 'text-green-600'
            : stock.changePercentage < 0
            ? 'text-red-600'
            : 'text-gray-600'
        }`}
      >
        {stock.changePercentage > 0 ? '+' : ''}
        {stock.changePercentage.toFixed(2)}%
      </span>
    </div>
  </div>
);