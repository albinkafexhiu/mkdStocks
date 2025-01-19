import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, TrendingDown, AlertCircle, Newspaper } from 'lucide-react';
import toast from 'react-hot-toast';
import { fundamentalApi } from '../api/fundamental';

const FundamentalAnalysisPage = () => {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [newsData, setNewsData] = useState<any>(null);
  const [marketSentiment, setMarketSentiment] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Fetch available symbols on mount
  useEffect(() => {
    const fetchSymbols = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/stocks/symbols');
        setSymbols(response.data);
      } catch (err) {
        toast.error('Failed to load symbols');
      }
    };
    fetchSymbols();
    fetchMarketSentiment();
  }, []);

  const fetchMarketSentiment = async () => {
    try {
      const data = await fundamentalApi.getMarketSentiment();
      setMarketSentiment(data);
    } catch (err) {
      console.error('Failed to fetch market sentiment:', err);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedSymbol) {
      toast.error('Please select a symbol');
      return;
    }

    setLoading(true);
    try {
      const [newsResponse, sentimentResponse] = await Promise.all([
        fundamentalApi.getLatestNews(selectedSymbol),
        fundamentalApi.getSentiment(selectedSymbol)
      ]);
      
      setNewsData({
        ...newsResponse,
        sentiment: sentimentResponse
      });
    } catch (err) {
      toast.error('Failed to fetch analysis');
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'BUY':
        return 'text-green-600';
      case 'SELL':
        return 'text-red-600';
      default:
        return 'text-yellow-600';
    }
  };

  // Render market sentiment overview
  const renderMarketOverview = () => {
    if (!marketSentiment) return null;

    const pieData = [
      { name: 'Buy', value: marketSentiment.recommendations.buy },
      { name: 'Hold', value: marketSentiment.recommendations.hold },
      { name: 'Sell', value: marketSentiment.recommendations.sell }
    ];

    const COLORS = ['#4ade80', '#facc15', '#ef4444'];

    return (
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Market Sentiment Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="h-64">
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-col justify-center">
            <p className="text-sm text-gray-600">Average Market Sentiment</p>
            <p className="text-2xl font-bold">{(marketSentiment.market_sentiment * 100).toFixed(1)}%</p>
            <p className="text-sm text-gray-600 mt-4">Companies Analyzed</p>
            <p className="text-xl">{marketSentiment.total_companies_analyzed}</p>
            <p className="text-sm text-gray-500 mt-2">Last Updated: {marketSentiment.analysis_date}</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-6">Fundamental Analysis</h1>

        {renderMarketOverview()}

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

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-blue-300"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {newsData && (
          <div className="space-y-6">
            {/* Company Sentiment Overview */}
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold">Company Sentiment</h3>
                  <p className={`text-2xl font-bold ${getSentimentColor(newsData.sentiment.recommendation)}`}>
                    {newsData.sentiment.recommendation}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">Sentiment Score</p>
                  <p className="text-xl font-semibold">
                    {(newsData.sentiment.average_sentiment * 100).toFixed(1)}%
                  </p>
                  <p className="text-sm text-gray-600">Based on {newsData.sentiment.article_count} articles</p>
                </div>
              </div>
            </div>

            {/* News List */}
            <div className="bg-white rounded-lg shadow">
              <h3 className="text-lg font-semibold p-4 border-b">Recent News</h3>
              <div className="divide-y">
                {newsData.latest_news.map((article: any, index: number) => (
                  <div key={index} className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="text-sm text-gray-600">{article.date}</p>
                        <h4 className="font-medium mt-1">{article.title.translated}</h4>
                        <p className="text-gray-600 mt-2 text-sm">{article.content.translated.slice(0, 200)}...</p>
                        <a 
                          href={article.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 text-sm mt-2 inline-block"
                        >
                          Read more →
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FundamentalAnalysisPage;