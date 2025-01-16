from src.filters.symbol_scraper import SymbolScraperFilter
from src.filters.date_checker import DateCheckerFilter

def test_date_checker():
    # Get symbols
    symbols = SymbolScraperFilter().process()
    
    # Check dates for first few symbols
    checker = DateCheckerFilter()
    for symbol in symbols[:5]:  # Test with first 5 symbols
        date_range = checker.process(symbol)
        print(f"\nSymbol: {symbol}")
        print(f"Start Date: {date_range['start_date']}")
        print(f"End Date: {date_range['end_date']}")

if __name__ == "__main__":
    test_date_checker()