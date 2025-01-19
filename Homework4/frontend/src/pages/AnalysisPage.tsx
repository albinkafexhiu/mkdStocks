import React from 'react';
import { useSymbols } from '../hooks/useSymbols';
import { useAnalysis } from '../hooks/useAnalysis';
import { AnalysisControls } from '../components/analysis/AnalysisControls';
import { PriceChart } from '../components/analysis/PriceChart';
import { OscillatorChart } from '../components/analysis/OscillatorChart';
import { AnalysisTable } from '../components/analysis/AnalysisTable';
import { PeriodOption } from '../types/analysis';

const AnalysisPage: React.FC = () => {
  const { 
    symbols, 
    selectedSymbol, 
    setSelectedSymbol, 
    loading: symbolsLoading 
  } = useSymbols();

  const {
    timeframe,
    setTimeframe,
    analysisResult,
    loading,
    activeTab,
    setActiveTab,
    handleAnalyze
  } = useAnalysis();

  const handleAnalyzeClick = () => {
    if (selectedSymbol) {
      handleAnalyze(selectedSymbol);
    }
  };

  return (
    <div className="p-6">
      <AnalysisControls 
        symbols={symbols}
        selectedSymbol={selectedSymbol}
        symbolsLoading={symbolsLoading}
        onSymbolChange={setSelectedSymbol}
        timeframe={timeframe}
        loading={loading}
        onTimeframeChange={setTimeframe}
        onAnalyze={handleAnalyzeClick}
      />

      {analysisResult && (
        <div className="space-y-6">
          <div className="flex gap-4 mb-4">
            {['daily', 'weekly', 'monthly'].map((period) => (
              <button
                key={period}
                onClick={() => setActiveTab(period as PeriodOption)}
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

          <PriceChart data={analysisResult[activeTab]} period={activeTab} />
          <OscillatorChart data={analysisResult[activeTab]} period={activeTab} />
          <AnalysisTable data={analysisResult[activeTab]} period={activeTab} />
        </div>
      )}
    </div>
  );
};

export default AnalysisPage;