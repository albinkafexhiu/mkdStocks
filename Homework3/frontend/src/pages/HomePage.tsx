import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Star } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

interface Stock {
  symbol: string;
  companyName: string;
  price: number;
  changePercentage: number;
}

interface SearchStock {
  symbol: string;
}

const HomePage = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchStock[]>([]);
  const [popularStocks, setPopularStocks] = useState<Stock[]>([]);
  const [wishlistStocks, setWishlistStocks] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSearchResults, setShowSearchResults] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (searchQuery) {
      handleSearch();
    } else {
      setSearchResults([]);
      setShowSearchResults(false);
    }
  }, [searchQuery]);

  const fetchData = async () => {
    try {
      const [popularResponse, wishlistResponse] = await Promise.all([
        axios.get('http://localhost:8000/api/stocks/popular-stocks'),
        axios.get('http://localhost:8000/api/stocks/wishlist')
      ]);

      setPopularStocks(popularResponse.data);
      setWishlistStocks(wishlistResponse.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
      toast.error('Failed to load stocks');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/stocks/symbols');
      const filteredStocks = response.data.filter((symbol: string) =>
        symbol.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setSearchResults(filteredStocks.map(symbol => ({ symbol })));
      setShowSearchResults(true);
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  const handleAddToWishlist = async (symbol: string) => {
    try {
      await axios.post(`http://localhost:8000/api/stocks/wishlist/${symbol}`);
      toast.success('Added to wishlist');
      fetchData(); // Refresh data
    } catch (error) {
      console.error('Failed to add to wishlist:', error);
      toast.error('Failed to add to wishlist');
    }
  };

  const handleRemoveFromWishlist = async (symbol: string) => {
    try {
      await axios.delete(`http://localhost:8000/api/stocks/wishlist/${symbol}`);
      toast.success('Removed from wishlist');
      fetchData(); // Refresh data
    } catch (error) {
      console.error('Failed to remove from wishlist:', error);
      toast.error('Failed to remove from wishlist');
    }
  };

  const isInWishlist = (symbol: string) => {
    return wishlistStocks.some(stock => stock.symbol === symbol);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'MKD',
      minimumFractionDigits: 2
    }).format(value);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-gray-600">Loading stocks...</div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Search Section */}
      <div className="mb-8 relative">
        <div className="flex items-center bg-white rounded-lg shadow-sm border border-gray-200">
          <Search className="h-5 w-5 text-gray-400 ml-4" />
          <input
            type="text"
            placeholder="Search stocks..."
            className="w-full p-4 focus:outline-none rounded-lg"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        {/* Search Results Dropdown */}
        {showSearchResults && searchResults.length > 0 && (
          <div className="absolute w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
            {searchResults.map((result) => (
              <div
                key={result.symbol}
                className="flex items-center justify-between p-4 hover:bg-gray-50 cursor-pointer"
                onClick={() => navigate(`/stocks/${result.symbol}`)}
              >
                <span className="font-medium">{result.symbol}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    isInWishlist(result.symbol)
                      ? handleRemoveFromWishlist(result.symbol)
                      : handleAddToWishlist(result.symbol);
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

      {/* Wishlist Section */}
      {wishlistStocks.length > 0 && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">My Watchlist</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {wishlistStocks.map((stock) => (
              <div
                key={stock.symbol}
                className="bg-white rounded-lg shadow-md p-6 cursor-pointer"
                onClick={() => navigate(`/stocks/${stock.symbol}`)}
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
                      handleRemoveFromWishlist(stock.symbol);
                    }}
                    className="p-2 hover:bg-gray-100 rounded-full"
                  >
                    <Star className="h-5 w-5 fill-yellow-400 text-yellow-400" />
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
            ))}
          </div>
        </div>
      )}

      {/* Popular Stocks Section */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Popular Stocks</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {popularStocks.map((stock) => (
            <div
              key={stock.symbol}
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer"
              onClick={() => navigate(`/stocks/${stock.symbol}`)}
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
                    isInWishlist(stock.symbol)
                      ? handleRemoveFromWishlist(stock.symbol)
                      : handleAddToWishlist(stock.symbol);
                  }}
                  className="p-2 hover:bg-gray-100 rounded-full"
                >
                  <Star
                    className={`h-5 w-5 ${
                      isInWishlist(stock.symbol)
                        ? 'fill-yellow-400 text-yellow-400'
                        : 'text-gray-400'
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
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;