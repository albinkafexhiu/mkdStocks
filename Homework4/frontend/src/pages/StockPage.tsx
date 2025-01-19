import React from 'react';
import { useParams } from 'react-router-dom';
import { useSymbols } from '../hooks/useSymbols';
import { StockDataViewer } from '../components/stocks/StockDataViewer';

const StockPage: React.FC = () => {
  const { symbol } = useParams();
  const { symbols, selectedSymbol, setSelectedSymbol, loading } = useSymbols(symbol);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <StockDataViewer 
        symbols={symbols}
        selectedSymbol={selectedSymbol}
        onSymbolChange={setSelectedSymbol}
        isLoading={loading}
      />
    </div>
  );
};

export default StockPage;