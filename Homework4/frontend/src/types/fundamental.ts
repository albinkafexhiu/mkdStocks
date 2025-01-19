export interface NewsArticle {
    date: string;
    title: {
      original: string;
      translated: string;
    };
    content: {
      original: string;
      translated: string;
    };
    url: string;
  }
  
  export interface SentimentData {
    symbol: string;
    company_name: string;
    average_sentiment: number;
    recommendation: 'BUY' | 'SELL' | 'HOLD';
    article_count: number;
  }
  
  export interface MarketSentiment {
    market_sentiment: number;
    recommendations: {
      buy: number;
      sell: number;
      hold: number;
    };
    total_companies_analyzed: number;
    analysis_date: string;
  }
  
  export interface NewsData {
    symbol: string;
    company_name: string;
    latest_news: NewsArticle[];
    sentiment: SentimentData;
  }