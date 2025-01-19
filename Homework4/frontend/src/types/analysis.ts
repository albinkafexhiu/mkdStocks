export interface AnalysisData {
    date: string;
    close: number;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    [key: string]: any; 
  }
  
  export interface AnalysisResult {
    daily: AnalysisData[];
    weekly: AnalysisData[];
    monthly: AnalysisData[];
  }
  
  export type TimeframeOption = '1M' | '3M' | '6M' | '1Y';
  export type PeriodOption = 'daily' | 'weekly' | 'monthly';