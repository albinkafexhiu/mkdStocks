import React from 'react';
import { TimeframeOption } from '../../types/analysis';
import { SymbolSelector } from '../common/SymbolSelector';

interface AnalysisControlsProps {
  symbols: string[];
  selectedSymbol: string;
  symbolsLoading: boolean;
  onSymbolChange: (symbol: string) => void;
  timeframe: TimeframeOption;
  loading: boolean;
  onTimeframeChange: (timeframe: TimeframeOption) => void;
  onAnalyze: () => void;
}

export const AnalysisControls: React.FC<AnalysisControlsProps> = ({
  symbols,
  selectedSymbol,
  symbolsLoading,
  onSymbolChange,
  timeframe,
  loading,
  onTimeframeChange,
  onAnalyze
}) => {
  const timeframes: TimeframeOption[] = ['1M', '3M', '6M', '1Y'];

  return (
    <div className="mb-6">
      <h1 className="text-2xl font-bold mb-6">Technical Analysis</h1>

      <div className="flex flex-wrap gap-4 mb-6">
        <div>
          <label className="block mb-2 font-medium">Symbol:</label>
          <SymbolSelector
            symbols={symbols}
            selectedSymbol={selectedSymbol}
            onSymbolChange={onSymbolChange}
            disabled={symbolsLoading}
            className="w-64"
          />
        </div>

        <div>
          <label className="block mb-2 font-medium">Timeframe:</label>
          <div className="flex space-x-2">
            {timeframes.map((tf) => (
              <button
                key={tf}
                onClick={() => onTimeframeChange(tf)}
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
        onClick={onAnalyze}
        disabled={loading || !selectedSymbol}
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-blue-300"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </div>
  );
};