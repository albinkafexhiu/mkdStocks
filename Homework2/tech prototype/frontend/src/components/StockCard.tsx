import React from 'react';
import { Star, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface StockCardProps {
  symbol: string;
  companyName: string;
  price: number;
  changePercentage: number;
  isFavorite?: boolean;
  onFavoriteToggle?: () => void;
}

const StockCard = ({ 
  symbol, 
  companyName, 
  price, 
  changePercentage, 
  isFavorite = false,
  onFavoriteToggle 
}: StockCardProps) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/stocks/${symbol}`);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'MKD',
      minimumFractionDigits: 2
    }).format(value);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 relative">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{companyName}</h3>
          <p className="text-2xl font-bold text-gray-900">{symbol}</p>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onFavoriteToggle?.();
          }}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
        >
          <Star 
            className={`h-6 w-6 ${isFavorite ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400'}`}
          />
        </button>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-baseline">
          <span className="text-xl font-semibold">{formatCurrency(price)}</span>
          <span className={`font-medium ${
            changePercentage > 0 ? 'text-green-600' : 
            changePercentage < 0 ? 'text-red-600' : 
            'text-gray-600'
          }`}>
            {changePercentage > 0 ? '+' : ''}{changePercentage.toFixed(2)}%
          </span>
        </div>
      </div>

      <button
        onClick={handleCardClick}
        className="absolute bottom-6 right-6 p-2 hover:bg-gray-100 rounded-full transition-colors"
      >
        <ChevronRight className="h-6 w-6 text-gray-400" />
      </button>
    </div>
  );
};

export default StockCard;