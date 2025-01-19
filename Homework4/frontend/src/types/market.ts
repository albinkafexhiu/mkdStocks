export interface MarketData {
    symbol: string;
    currentPrice: number;
    startPrice: number;
    priceChange: number;
    totalVolume: number;
    totalTurnover: number;
    lastTradeDate: string;
  }
  
  export interface MarketStats {
    totalTurnover: number;
    totalVolume: number;
    gainers: number;
    losers: number;
  }