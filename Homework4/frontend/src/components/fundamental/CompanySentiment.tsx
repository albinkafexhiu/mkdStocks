import React from 'react';
import { SentimentData } from '../../types/fundamental';

interface CompanySentimentProps {
  sentiment: SentimentData;
}

export const CompanySentiment: React.FC<CompanySentimentProps> = ({ sentiment }) => {
  const getSentimentColor = (recommendation: string) => {
    switch (recommendation) {
      case 'BUY':
        return 'text-green-600';
      case 'SELL':
        return 'text-red-600';
      default:
        return 'text-yellow-600';
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">Company Sentiment</h3>
          <p className={`text-2xl font-bold ${getSentimentColor(sentiment.recommendation)}`}>
            {sentiment.recommendation}
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Sentiment Score</p>
          <p className="text-xl font-semibold">
            {(sentiment.average_sentiment * 100).toFixed(1)}%
          </p>
          <p className="text-sm text-gray-600">Based on {sentiment.article_count} articles</p>
        </div>
      </div>
    </div>
  );
};