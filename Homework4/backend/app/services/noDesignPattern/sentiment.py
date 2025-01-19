from transformers import pipeline, MarianMTModel, MarianTokenizer
import json
from datetime import datetime
from typing import Dict, List, Any

class SentimentAnalyzer:
    def __init__(self):
        # Initialize translation models
        self.translator_tokenizer = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-mk-en')
        self.translator_model = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-mk-en')
        
        # Initialize sentiment analyzer (FinBERT for financial texts)
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="yiyanghkust/finbert-tone",
            return_all_scores=True
        )

    def translate_text(self, text: str, max_length: int = 512) -> str:
        """Translate Macedonian text to English"""
        # Split text into manageable chunks
        words = text.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            if len(' '.join(current_chunk + [word])) <= max_length:
                current_chunk.append(word)
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        translated_chunks = []
        for chunk in chunks:
            # Translate each chunk
            encoded = self.translator_tokenizer(chunk, return_tensors="pt", padding=True)
            translated = self.translator_model.generate(**encoded)
            decoded = self.translator_tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_chunks.append(decoded)
            
        return ' '.join(translated_chunks)

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of English text"""
        results = self.sentiment_analyzer(text[:512])[0]
        
        # Get sentiment with highest score
        sentiment = max(results, key=lambda x: x['score'])
        
        return {
            'sentiment': sentiment['label'],
            'score': sentiment['score'],
            'recommendation': 'BUY' if sentiment['label'] == 'Positive' 
                            else 'SELL' if sentiment['label'] == 'Negative' 
                            else 'HOLD'
        }

    def process_news_file(self, input_filename: str) -> None:
        """Process scraped news file - translate and analyze sentiment"""
        with open(input_filename, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
            
        analyzed_data = {}
        
        for company, articles in news_data.items():
            print(f"Processing articles for {company}")
            processed_articles = []
            
            for article in articles:
                # Translate title and content
                translated_title = self.translate_text(article['title'])
                translated_content = self.translate_text(article['content'])
                
                # Analyze sentiment
                sentiment_result = self.analyze_sentiment(translated_content)
                
                processed_articles.append({
                    'date': article['date'],
                    'title': {
                        'original': article['title'],
                        'translated': translated_title
                    },
                    'content': {
                        'original': article['content'],
                        'translated': translated_content
                    },
                    'sentiment': sentiment_result,
                    'url': article['url'],
                    'source': article['source']
                })
            
            # Calculate overall sentiment for company
            if processed_articles:
                avg_sentiment = sum(article['sentiment']['score'] for article in processed_articles) / len(processed_articles)
                overall_recommendation = 'BUY' if avg_sentiment > 0.6 else 'SELL' if avg_sentiment < 0.4 else 'HOLD'
            else:
                avg_sentiment = 0
                overall_recommendation = 'HOLD'
            
            analyzed_data[company] = {
                'articles': processed_articles,
                'average_sentiment': avg_sentiment,
                'overall_recommendation': overall_recommendation
            }
            
        # Save analyzed data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f'analyzed_news_{timestamp}.json'
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(analyzed_data, f, ensure_ascii=False, indent=2)
            
        print(f"Analysis completed and saved to {output_filename}")

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    # Get most recent scraped news file
    import glob
    latest_news_file = max(glob.glob('scraped_news_*.json'))
    analyzer.process_news_file(latest_news_file)