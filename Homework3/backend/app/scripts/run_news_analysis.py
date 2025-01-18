from app.services.news_processor import NewsProcessor

def main():
    processor = NewsProcessor()
    processor.process_news()

if __name__ == "__main__":
    main()