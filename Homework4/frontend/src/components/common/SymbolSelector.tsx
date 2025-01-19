import React from 'react';

interface SymbolSelectorProps {
  symbols: string[];
  selectedSymbol: string;
  onSymbolChange: (symbol: string) => void;
  className?: string;
  disabled?: boolean;
}

export const SymbolSelector: React.FC<SymbolSelectorProps> = ({
  symbols,
  selectedSymbol,
  onSymbolChange,
  className = '',
  disabled = false
}) => (
  <select
    value={selectedSymbol}
    onChange={(e) => onSymbolChange(e.target.value)}
    className={`w-full md:w-64 rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 ${className}`}
    disabled={disabled}
  >
    <option value="">-- Select Symbol --</option>
    {symbols.map((sym) => (
      <option key={sym} value={sym}>{sym}</option>
    ))}
  </select>
);