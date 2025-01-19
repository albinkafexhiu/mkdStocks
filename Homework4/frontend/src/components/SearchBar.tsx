import React from 'react';
import { Search, Star } from 'lucide-react';
import { SearchStock } from '../types/stock';

interface SearchBarProps {
  searchQuery: string;
  onSearchChange: (value: string) => void;
  searchResults: SearchStock[];
  showResults: boolean;
  isInWishlist: (symbol: string) => boolean;
  onStockSelect: (symbol: string) => void;
  onWishlistToggle: (symbol: string) => Promise<void>;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  searchQuery,
  onSearchChange,
  searchResults,
  showResults,
  isInWishlist,
  onStockSelect,
  onWishlistToggle,
}) => (
  <div className="mb-8 relative">
    <div className="flex items-center bg-white rounded-lg shadow-sm border border-gray-200">
      <Search className="h-5 w-5 text-gray-400 ml-4" />
      <input
        type="text"
        placeholder="Search stocks..."
        className="w-full p-4 focus:outline-none rounded-lg"
        value={searchQuery}
        onChange={(e) => onSearchChange(e.target.value)}
      />
    </div>

    {showResults && searchResults.length > 0 && (
      <div className="absolute w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
        {searchResults.map((result) => (
          <div
            key={result.symbol}
            className="flex items-center justify-between p-4 hover:bg-gray-50 cursor-pointer"
            onClick={() => onStockSelect(result.symbol)}
          >
            <span className="font-medium">{result.symbol}</span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onWishlistToggle(result.symbol);
              }}
              className="p-2 hover:bg-gray-100 rounded-full"
            >
              <Star
                className={`h-5 w-5 ${
                  isInWishlist(result.symbol)
                    ? 'fill-yellow-400 text-yellow-400'
                    : 'text-gray-400'
                }`}
              />
            </button>
          </div>
        ))}
      </div>
    )}
  </div>
);
