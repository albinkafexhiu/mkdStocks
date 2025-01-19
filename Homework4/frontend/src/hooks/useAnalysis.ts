import { useState } from 'react';
import { analysisApi } from '../api/analysis';
import { TimeframeOption, PeriodOption, AnalysisResult } from '../types/analysis';
import toast from 'react-hot-toast';

export const useAnalysis = () => {
  const [timeframe, setTimeframe] = useState<TimeframeOption>('6M');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<PeriodOption>('daily');

  const handleAnalyze = async (symbol: string) => {
    if (!symbol) {
      toast.error("Select a symbol");
      return;
    }
    setLoading(true);
    try {
      const data = await analysisApi.getTechnicalAnalysis(symbol, timeframe);
      setAnalysisResult(data);
    } catch (err) {
      toast.error("Analysis failed");
      console.error("Analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  return {
    timeframe,
    setTimeframe,
    analysisResult,
    loading,
    activeTab,
    setActiveTab,
    handleAnalyze
  };
};