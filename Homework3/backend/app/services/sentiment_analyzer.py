from transformers import pipeline
from typing import Dict, Any, Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="yiyanghkust/finbert-tone",  # Using FinBERT for financial text
            return_all_scores=True
        )

    def analyze_text(self, text: str) -> Dict[str, Any]:
        results = self.analyzer(text[:512])[0]  # Analyze first 512 tokens
        
        # Get highest scoring sentiment
        sentiment = max(results, key=lambda x: x['score'])
        
        # Map sentiment to trading signal
        sentiment_mapping = {
            'Positive': 'BUY',
            'Negative': 'SELL',
            'Neutral': 'HOLD'
        }
        
        return {
            'sentiment': sentiment['label'],
            'score': sentiment['score'],
            'recommendation': sentiment_mapping[sentiment['label']]
        }

    def get_overall_sentiment(self, sentiment_scores: List[Dict[str, float]]) -> str:
        if not sentiment_scores:
            return 'HOLD'
            
        avg_score = sum(s['score'] for s in sentiment_scores) / len(sentiment_scores)
        if avg_score > 0.6:
            return 'BUY'
        elif avg_score < 0.4:
            return 'SELL'
        return 'HOLD'