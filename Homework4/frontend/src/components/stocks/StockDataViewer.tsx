import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useStockData } from '../../hooks/useStockData';
import { SymbolSelector } from '../common/SymbolSelector';
import { TimeRangeSelector } from './TimeRangeSelector';
import { StockChart } from './StockChart';
import { StockDataTable } from './StockDataTable';

interface StockDataViewerProps {
  symbols: string[];
  selectedSymbol: string;
  onSymbolChange: (symbol: string) => void;
  isLoading: boolean;
}

const timeRanges = [
  { label: '1D', days: 1 },
  { label: '1W', days: 7 },
  { label: '1M', days: 30 },
  { label: '1Y', days: 365 },
  { label: '5Y', days: 1825 },
  { label: '10Y', days: 3650 }
];

export const StockDataViewer: React.FC<StockDataViewerProps> = ({
  symbols,
  selectedSymbol,
  onSymbolChange,
  isLoading
}) => {
  const navigate = useNavigate();
  const {
    startDate,
    setStartDate,
    endDate,
    setEndDate,
    stockData,
    loading: dataLoading,
    fetchStockData,
    handleTimeRangeSelect
  } = useStockData();

  const handleSymbolSelect = (value: string) => {
    onSymbolChange(value);
    if (value) {
      navigate(`/stocks/${value}`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedSymbol) {
      await fetchStockData(selectedSymbol);
    }
  };

  const handleTimeRange = (days: number) => {
    handleTimeRangeSelect(days);
    if (selectedSymbol) {
      fetchStockData(selectedSymbol);
    }
  };

  return (
    <div className="mb-8 bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Stock Data Analysis</h2>
      
      <div className="mb-6">
        <SymbolSelector
          symbols={symbols}
          selectedSymbol={selectedSymbol}
          onSymbolChange={handleSymbolSelect}
          disabled={isLoading}
        />
      </div>

      {selectedSymbol && (
        <>
          <TimeRangeSelector 
            timeRanges={timeRanges}
            onSelect={handleTimeRange}
          />

          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div className="flex items-end">
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 
                         transition-colors duration-200 focus:outline-none focus:ring-2 
                         focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
                disabled={dataLoading}
              >
                {dataLoading ? 'Loading...' : 'Update Chart'}
              </button>
            </div>
          </form>
        </>
      )}

      {stockData.length > 0 && (
        <div className="space-y-6 mt-6">
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              {selectedSymbol} - Price History
            </h3>
            <StockChart data={stockData} />
          </div>

          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Detailed Data</h3>
            <StockDataTable data={stockData} />
          </div>
        </div>
      )}
    </div>
  );
};