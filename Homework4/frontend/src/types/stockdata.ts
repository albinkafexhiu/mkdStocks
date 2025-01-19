export interface TimeRange {
    label: string;
    days: number;
  }
  
  export interface StockData {
    date: string;
    lastTradePrice: number;
    maxPrice: number;
    minPrice: number;
    changePercentage: number;
    volume: number;
    avgPrice: number;
    turnoverBest: number;
    totalTurnover: number;
  }