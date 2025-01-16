from src.filters.symbol_scraper import SymbolScraperFilter
from src.filters.date_checker import DateCheckerFilter
from src.filters.data_fetcher import DataFetcherFilter

def test_data_fetcher():
    # Get first symbol
    symbols = SymbolScraperFilter().process()
    first_symbol = symbols[0]  # Test with ADIN

    # Get date range
    date_range = DateCheckerFilter().process(first_symbol)
    
    # Fetch data
    fetcher = DataFetcherFilter()
    data = fetcher.process(date_range)
    
    # Print first few records
    print(f"\nFirst 5 records for {first_symbol}:")
    for record in data[:5]:
        print(record)

if __name__ == "__main__":
    test_data_fetcher()