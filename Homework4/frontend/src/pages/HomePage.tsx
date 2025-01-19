import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchBar } from '../components/SearchBar';
import { StockCard } from '../components/common/StockCard';
import { useStocks } from '../hooks/useStocks';
import { useStockSearch } from '../hooks/useStockSearch';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const {
    popularStocks,
    wishlistStocks,
    loading,
    handleAddToWishlist,
    handleRemoveFromWishlist,
    isInWishlist,
  } = useStocks();

  const {
    searchQuery,
    setSearchQuery,
    searchResults,
    showSearchResults,
  } = useStockSearch();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-gray-600">Loading stocks...</div>
      </div>
    );
  }

  const handleWishlistToggle = async (symbol: string): Promise<void> => {
    if (isInWishlist(symbol)) {
      await handleRemoveFromWishlist(symbol);
    } else {
      await handleAddToWishlist(symbol);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <SearchBar
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        searchResults={searchResults}
        showResults={showSearchResults}
        isInWishlist={isInWishlist}
        onStockSelect={(symbol) => navigate(`/stocks/${symbol}`)}
        onWishlistToggle={handleWishlistToggle}
      />

      {wishlistStocks.length > 0 && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">My Watchlist</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {wishlistStocks.map((stock) => (
              <StockCard
                key={stock.symbol}
                stock={stock}
                isInWishlist={true}
                onWishlistToggle={handleRemoveFromWishlist}
                onClick={() => navigate(`/stocks/${stock.symbol}`)}
              />
            ))}
          </div>
        </div>
      )}

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Popular Stocks</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {popularStocks.map((stock) => (
            <StockCard
              key={stock.symbol}
              stock={stock}
              isInWishlist={isInWishlist(stock.symbol)}
              onWishlistToggle={handleWishlistToggle}
              onClick={() => navigate(`/stocks/${stock.symbol}`)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;