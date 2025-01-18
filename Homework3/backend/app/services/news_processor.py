import json
from datetime import datetime
from typing import Dict, List, Any
from .news_scraper import NewsScraper
from .translator import Translator
from .sentiment_analyzer import SentimentAnalyzer

class NewsProcessor:
    def __init__(self):
        self.scraper = NewsScraper()
        self.translator = Translator()
        self.sentiment_analyzer = SentimentAnalyzer()
        
    def process_news(self) -> None:
        """
        Main function to scrape, translate, analyze and save news data
        """
        news_data = {}
        
        # Get news for all companies
        raw_news = self.scraper.scrape_all_news()
        
        for company, articles in raw_news.items():
            processed_articles = []
            
            for article in articles:
                # Translate title and content
                translated_title = self.translator.translate_text(article['title'])
                translated_content = self.translator.translate_text(article['content'])
                
                # Analyze sentiment
                sentiment_result = self.sentiment_analyzer.analyze_text(translated_content)
                
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
            
            news_data[company] = {
                'articles': processed_articles,
                'overall_sentiment': self.sentiment_analyzer.get_overall_sentiment(
                    [article['sentiment'] for article in processed_articles]
                )
            }
        
        # Save to file
        self._save_news_data(news_data)
    
    def _save_news_data(self, data: Dict[str, Any]) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"news_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)