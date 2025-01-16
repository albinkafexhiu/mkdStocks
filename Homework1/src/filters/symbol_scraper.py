import requests
from bs4 import BeautifulSoup

class SymbolScraperFilter:
    def __init__(self):
        self.base_url = "https://www.mse.mk/en/stats/symbolhistory/adin"  

    def process(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()  
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            dropdown = soup.find('select', {'id': 'Code'})
            
            if not dropdown:
                raise Exception("Could not find symbol dropdown")
            
            symbols = []
            for option in dropdown.find_all('option'):
                symbol = option['value']
                # Skip symbols containing numbers 
                if not any(char.isdigit() for char in symbol):
                    symbols.append(symbol)
            
            print(f"Found {len(symbols)} valid symbols")
            return symbols
            
        except Exception as e:
            print(f"Error scraping symbols: {e}")
            return []