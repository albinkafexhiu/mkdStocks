from typing import Dict, Any
from transformers import pipeline
from .base_processor import NewsProcessor

class SentimentProcessor(NewsProcessor):
    def __init__(self):
        super().__init__()
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="yiyanghkust/finbert-tone",
            return_all_scores=True
        )

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        results = self.sentiment_analyzer(text[:512])[0]
        sentiment = max(results, key=lambda x: x['score'])
        
        return {
            'sentiment': sentiment['label'],
            'score': sentiment['score'],
            'recommendation': 'BUY' if sentiment['label'] == 'Positive' 
                            else 'SELL' if sentiment['label'] == 'Negative' 
                            else 'HOLD'
        }

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        analyzed_data = {}
        
        for company, articles in data.items():
            processed_articles = []
            total_sentiment = 0
            
            for article in articles:
                sentiment_result = self.analyze_sentiment(article['content']['translated'])
                article['sentiment'] = sentiment_result
                processed_articles.append(article)
                total_sentiment += sentiment_result['score']
            
            avg_sentiment = total_sentiment / len(articles) if articles else 0
            overall_recommendation = 'BUY' if avg_sentiment > 0.6 else 'SELL' if avg_sentiment < 0.4 else 'HOLD'
            
            analyzed_data[company] = {
                'articles': processed_articles,
                'average_sentiment': avg_sentiment,
                'overall_recommendation': overall_recommendation
            }
        
        return self.process_next(analyzed_data)