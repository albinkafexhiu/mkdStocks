import React from 'react';
import { SymbolSelector } from '../common/SymbolSelector';

interface AnalysisControlsProps {
  symbols: string[];
  selectedSymbol: string;
  onSymbolChange: (symbol: string) => void;
  onAnalyze: () => void;
  loading: boolean;
  symbolsLoading: boolean;
}

export const AnalysisControls: React.FC<AnalysisControlsProps> = ({
  symbols,
  selectedSymbol,
  onSymbolChange,
  onAnalyze,
  loading,
  symbolsLoading,
}) => (
  <div className="flex flex-wrap gap-4 mb-6">
    <div>
      <label className="block mb-2 font-medium">Symbol:</label>
      <SymbolSelector
        symbols={symbols}
        selectedSymbol={selectedSymbol}
        onSymbolChange={onSymbolChange}
        disabled={symbolsLoading}
      />
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