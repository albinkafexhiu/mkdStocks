import React, { useState, useEffect } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import { analysisApi } from "../api/analysis";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, TrendingUp, TrendingDown, Calendar } from "lucide-react";

const AnalysisPage = () => {
  const [symbols, setSymbols] = useState([]);
  const [selectedSymbol, setSelectedSymbol] = useState("");
  const [timeframe, setTimeframe] = useState("6M");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("daily");

  useEffect(() => {
    (async () => {
      try {
        const resp = await axios.get("http://localhost:8000/api/stocks/symbols");
        setSymbols(resp.data);
      } catch (err) {
        toast.error("Could not load symbols");
      }
    })();
  }, []);

  const handleAnalyze = async () => {
    if (!selectedSymbol) {
      toast.error("Select a symbol");
      return;
    }
    setLoading(true);
    try {
      const data = await analysisApi.getTechnicalAnalysis(selectedSymbol, timeframe);
      setAnalysisResult(data);
    } catch (err) {
      toast.error("Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const getSignalColor = (signal) => {
    switch (signal?.toUpperCase()) {
      case 'BUY':
        return 'text-green-600';
      case 'SELL':
        return 'text-red-600';
      default:
        return 'text-yellow-600';
    }
  };

  const renderPriceChart = (data, period) => {
    if (!data || data.length === 0) return null;

    return (
      <div className="h-96 w-full mt-4 bg-white p-4 rounded-lg shadow">
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis 
              yAxisId="price"
              orientation="right"
              domain={['auto', 'auto']}
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              yAxisId="indicator"
              orientation="left"
              domain={[0, 100]}
              tick={{ fontSize: 12 }}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: 'white', border: '1px solid #ccc' }}
            />
            <Legend />
            <Line
              yAxisId="price"
              type="monotone"
              dataKey="close"
              stroke="#2563eb"
              dot={false}
              name="Price"
            />
            <Line
              yAxisId="price"
              type="monotone"
              dataKey={`sma_${period}`}
              stroke="#16a34a"
              dot={false}
              name="SMA"
            />
            <Line
              yAxisId="price"
              type="monotone"
              dataKey={`ema_${period}`}
              stroke="#9333ea"
              dot={false}
              name="EMA"
            />
            <Line
              yAxisId="indicator"
              type="monotone"
              dataKey={`rsi_${period}`}
              stroke="#dc2626"
              dot={false}
              name="RSI"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderOscillatorChart = (data, period) => {
    if (!data || data.length === 0) return null;

    return (
      <div className="h-96 w-full mt-4 bg-white p-4 rounded-lg shadow">
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis 
              domain={[0, 100]}
              tick={{ fontSize: 12 }}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: 'white', border: '1px solid #ccc' }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey={`stoch_k_${period}`}
              stroke="#2563eb"
              dot={false}
              name="Stochastic %K"
            />
            <Line
              type="monotone"
              dataKey={`stoch_d_${period}`}
              stroke="#16a34a"
              dot={false}
              name="Stochastic %D"
            />
            <Line
              type="monotone"
              dataKey={`mfi_${period}`}
              stroke="#9333ea"
              dot={false}
              name="MFI"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderDataTable = (data, period) => {
    if (!data || data.length === 0) return null;

    return (
      <div className="overflow-x-auto mt-4">
        <table className="min-w-full bg-white rounded-lg shadow">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3 text-left">Date</th>
              <th className="p-3 text-left">Close</th>
              <th className="p-3 text-left">RSI</th>
              <th className="p-3 text-left">Stoch K</th>
              <th className="p-3 text-left">Stoch D</th>
              <th className="p-3 text-left">MFI</th>
              <th className="p-3 text-left">Signal</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx} className="border-t hover:bg-gray-50">
                <td className="p-3">{row.date}</td>
                <td className="p-3">{row.close?.toFixed(2)}</td>
                <td className="p-3">{row[`rsi_${period}`]?.toFixed(2)}</td>
                <td className="p-3">{row[`stoch_k_${period}`]?.toFixed(2)}</td>
                <td className="p-3">{row[`stoch_d_${period}`]?.toFixed(2)}</td>
                <td className="p-3">{row[`mfi_${period}`]?.toFixed(2)}</td>
                <td className={`p-3 font-semibold ${getSignalColor(row[`signal_${period}`])}`}>
                  {row[`signal_${period}`]}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-6">Technical Analysis</h1>

        <div className="flex flex-wrap gap-4 mb-6">
          <div>
            <label className="block mb-2 font-medium">Symbol:</label>
            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className="border border-gray-300 rounded px-3 py-2 w-64"
            >
              <option value="">-- Select Symbol --</option>
              {symbols.map((sym) => (
                <option key={sym} value={sym}>{sym}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-2 font-medium">Timeframe:</label>
            <div className="flex space-x-2">
              {["1M", "3M", "6M", "1Y"].map((tf) => (
                <button
                  key={tf}
                  onClick={() => setTimeframe(tf)}
                  className={`px-4 py-2 rounded border ${
                    timeframe === tf
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 hover:bg-gray-200"
                  }`}
                >
                  {tf}
                </button>
              ))}
            </div>
          </div>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-blue-300"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {analysisResult && (
        <div className="space-y-6">
          <div className="flex gap-4 mb-4">
            {["daily", "weekly", "monthly"].map((period) => (
              <button
                key={period}
                onClick={() => setActiveTab(period)}
                className={`px-4 py-2 rounded-t-lg border-b-2 ${
                  activeTab === period
                    ? "border-blue-600 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                {period.charAt(0).toUpperCase() + period.slice(1)}
              </button>
            ))}
          </div>

          {renderPriceChart(analysisResult[activeTab], activeTab)}
          {renderOscillatorChart(analysisResult[activeTab], activeTab)}
          {renderDataTable(analysisResult[activeTab], activeTab)}
        </div>
      )}
    </div>
  );
};

export default AnalysisPage;