import React from 'react';
import { useFundamental } from '../hooks/useFundamental';
import { MarketOverview } from '../components/fundamental/MarketOverview';
import { CompanySentiment } from '../components/fundamental/CompanySentiment';
import { NewsList } from '../components/fundamental/NewsList';
import { AnalysisControls } from '../components/fundamental/AnalysisControls';

const FundamentalAnalysisPage: React.FC = () => {
  const {
    symbols,
    selectedSymbol,
    setSelectedSymbol,
    newsData,
    marketSentiment,
    loading,
    symbolsLoading,
    handleAnalyze
  } = useFundamental();

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-6">Fundamental Analysis</h1>

        {marketSentiment && <MarketOverview data={marketSentiment} />}

        <AnalysisControls
          symbols={symbols}
          selectedSymbol={selectedSymbol}
          onSymbolChange={setSelectedSymbol}
          onAnalyze={handleAnalyze}
          loading={loading}
          symbolsLoading={symbolsLoading}
        />

        {newsData && (
          <div className="space-y-6">
            <CompanySentiment sentiment={newsData.sentiment} />
            <NewsList articles={newsData.latest_news} />
          </div>
        )}
      </div>
    </div>
  );
};

export default FundamentalAnalysisPage;