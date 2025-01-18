import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import toast from 'react-hot-toast';

interface TimeRange {
  label: string;
  days: number;
}

const StockDataViewer = () => {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState(symbol || '');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [stockData, setStockData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const timeRanges: TimeRange[] = [
    { label: '1D', days: 1 },
    { label: '1W', days: 7 },
    { label: '1M', days: 30 },
    { label: '1Y', days: 365 },
    { label: '5Y', days: 1825 },
    { label: '10Y', days: 3650 }
  ];

  useEffect(() => {
    const fetchSymbols = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/stocks/symbols');
        setSymbols(response.data);
      } catch (error) {
        toast.error('Failed to fetch stock symbols');
      }
    };
    fetchSymbols();
  }, []);

  useEffect(() => {
    if (symbol) {
      setSelectedSymbol(symbol);
      // Auto-load last month's data when symbol is provided in URL
      const end = new Date();
      const start = new Date();
      start.setMonth(start.getMonth() - 1);
      
      setStartDate(start.toISOString().split('T')[0]);
      setEndDate(end.toISOString().split('T')[0]);
      
      fetchStockData(symbol, start.toISOString().split('T')[0], end.toISOString().split('T')[0]);
    }
  }, [symbol]);

  const fetchStockData = async (stockSymbol: string, start: string, end: string) => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/stocks/data/${stockSymbol}`, {
        params: { start_date: start, end_date: end }
      });
      setStockData(response.data);
      toast.success('Data loaded successfully');
    } catch (error) {
      toast.error('Failed to fetch stock data');
    } finally {
      setLoading(false);
    }
  };

  const handleSymbolSelect = (value: string) => {
    setSelectedSymbol(value);
    if (value) {
      navigate(`/stocks/${value}`);
    }
  };

  const handleTimeRangeSelect = (days: number) => {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);
    
    setStartDate(start.toISOString().split('T')[0]);
    setEndDate(end.toISOString().split('T')[0]);
    
    fetchStockData(selectedSymbol, start.toISOString().split('T')[0], end.toISOString().split('T')[0]);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedSymbol) {
      fetchStockData(selectedSymbol, startDate, endDate);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="mb-8 bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">Stock Data Analysis</h2>
        
        {/* Symbol Selection */}
        <div className="mb-6">
          <select
            value={selectedSymbol}
            onChange={(e) => handleSymbolSelect(e.target.value)}
            className="w-full md:w-1/3 rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Select a symbol</option>
            {symbols.map((sym) => (
              <option key={sym} value={sym}>{sym}</option>
            ))}
          </select>
        </div>

        {selectedSymbol && (
          <>
            {/* Time Range Buttons */}
            <div className="flex flex-wrap gap-2 mb-6">
              {timeRanges.map((range) => (
                <button
                  key={range.label}
                  onClick={() => handleTimeRangeSelect(range.days)}
                  className="px-4 py-2 rounded-lg bg-blue-100 hover:bg-blue-200 text-blue-700 font-medium"
                >
                  {range.label}
                </button>
              ))}
            </div>

            {/* Custom Date Range */}
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
                  disabled={loading}
                >
                  {loading ? 'Loading...' : 'Update Chart'}
                </button>
              </div>
            </form>
          </>
        )}
      </div>

      {stockData.length > 0 && (
        <div className="space-y-6">
          {/* Chart Section */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              {selectedSymbol} - Price History
            </h3>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={stockData}>
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
          </div>

          {/* Table Section */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Detailed Data</h3>
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
                  {stockData.map((data, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{data.date}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{data.lastTradePrice.toFixed(2)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{data.maxPrice.toFixed(2)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{data.minPrice.toFixed(2)}</td>
                      <td className={`px-6 py-4 whitespace-nowrap text-sm ${data.changePercentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {data.changePercentage.toFixed(2)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{data.volume.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockDataViewer;