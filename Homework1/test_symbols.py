from src.filters.symbol_scraper import SymbolScraperFilter

def test_symbol_scraper():
    scraper = SymbolScraperFilter()
    symbols = scraper.process()
    print("\nSymbols found:")
    for symbol in symbols:
        print(symbol)

if __name__ == "__main__":
    test_symbol_scraper()