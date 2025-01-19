import json
from datetime import datetime
from typing import List, Dict, Any
from .scrapers.kapital_scraper import KapitalScraper
from .scrapers.biznis_scraper import BiznisInfoScraper
from .processors.translator_processor import TranslatorProcessor
from .processors.sentiment_processor import SentimentProcessor

class NewsService:
    def __init__(self, articles_per_source: int = 3):
        self.articles_per_source = articles_per_source
        
        # Initialize scrapers
        self.scrapers = [
            KapitalScraper(articles_per_source),
            BiznisInfoScraper(articles_per_source)
        ]
        
        # Set up processing chain
        self.translator = TranslatorProcessor()
        self.sentiment_analyzer = SentimentProcessor()
        self.translator.set_next(self.sentiment_analyzer)

    def scrape_company_news(self, company: str) -> List[Dict[str, Any]]:
        all_articles = []
        for scraper in self.scrapers:
            articles = scraper.scrape_company_news(company)
            all_articles.extend(articles)
        return all_articles

    def process_news(self, companies: List[str]) -> None:
        all_news = {}
        total_companies = len(companies)
        
        print(f"Starting news analysis for {total_companies} companies...")
        print(f"Will get {self.articles_per_source} articles per source (total {self.articles_per_source * len(self.scrapers)} per company)")
        
        for i, company in enumerate(companies, 1):
            print(f"\nProgress: {i}/{total_companies} companies")
            print(f"Starting news scrape for: {company}")
            
            try:
                company_news = self.scrape_company_news(company)
                if company_news:
                    all_news[company] = company_news
                print(f"Total articles found for {company}: {len(company_news)}")
            except Exception as e:
                print(f"Error processing {company}: {str(e)}")
        
        # Process through the chain
        processed_data = self.translator.process(all_news)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'analyzed_news_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
            
        print(f"\nNews analysis completed!")
        print(f"Results saved to: {filename}")
        print(f"Total companies processed: {len(processed_data)}")