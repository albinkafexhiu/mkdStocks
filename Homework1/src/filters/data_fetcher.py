import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import json
import os
import hashlib
import pandas as pd

class DataFetcherFilter:
    def __init__(self):
        self.base_url = "https://www.mse.mk/en/stats/symbolhistory"
        self.retry_strategy = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504, 429],
            allowed_methods=["GET"]
        )
        self.timeout = (5, 15)
        
        # Ensure directories exist
        self.raw_dir = os.path.join("data", "raw")
        self.processed_dir = os.path.join("data", "processed")
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs("data/csv", exist_ok=True)  # Create csv directory

    def _generate_filename(self, symbol, start_date, end_date):
        """Generate a unique filename for the data"""
        date_str = f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"
        hash_str = hashlib.md5(f"{symbol}-{date_str}".encode()).hexdigest()[:8]
        return f"{symbol}_{date_str}_{hash_str}"

    def _save_raw_data(self, symbol, start_date, end_date, content):
        """Save raw HTML content"""
        filename = self._generate_filename(symbol, start_date, end_date)
        filepath = os.path.join(self.raw_dir, f"{filename}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def _format_price(self, value):
        """Format price with proper separators"""
        try:
            formatted = f"{float(value):,.2f}"
            return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "0,00"

    def _format_number(self, value):
        """Format whole numbers"""
        try:
            return f"{int(float(value)):,}".replace(",", ".")
        except (ValueError, TypeError):
            return "0"

    def _save_to_csv(self, symbol, data):
        """Save data to CSV format"""
        columns = ['Date', 'Last trade price', 'Max', 'Min', 'Avg. Price', 
                  '%chg.', 'Volume', 'Turnover in BEST', 'Total turnover']
        
        csv_data = []
        for row in data:
            csv_row = [
                row['date'].strftime('%d.%m.%Y'),
                self._format_price(row['last_trade_price']),
                self._format_price(row['max_price']),
                self._format_price(row['min_price']),
                self._format_price(row['avg_price']),
                self._format_price(row['change_percentage']),
                self._format_number(row['volume']),
                self._format_number(row['turnover_best']),
                self._format_number(row['total_turnover'])
            ]
            csv_data.append(csv_row)

        df = pd.DataFrame(csv_data, columns=columns)
        filepath = f"data/csv/{symbol}.csv"
        df.to_csv(filepath, index=False)

    def _save_processed_data(self, symbol, start_date, end_date, data):
        """Save processed data as JSON"""
        filename = self._generate_filename(symbol, start_date, end_date)
        filepath = os.path.join(self.processed_dir, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, default=str, indent=2)

    def process(self, input_data, session=None):
        if session is None:
            session = self._create_session()
        
        symbol = input_data['symbol']
        start_date = input_data['start_date']
        end_date = input_data['end_date']

        try:
            url = f"{self.base_url}/{symbol}"
            params = {
                'fromDate': start_date.strftime('%m/%d/%Y'),
                'toDate': end_date.strftime('%m/%d/%Y')
            }

            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Fetching data for {symbol} "
                  f"from {start_date} to {end_date}")

            # Add exponential backoff for retries
            response_content = None
            for attempt in range(3):
                try:
                    request_start = time.time()
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Making request for {symbol} (attempt {attempt + 1})")
                    response = session.get(url, params=params, timeout=self.timeout)
                    request_duration = time.time() - request_start
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Request for {symbol} completed in {request_duration:.2f}s "
                          f"(Status: {response.status_code})")
                    response.raise_for_status()
                    response_content = response.text
                    self._save_raw_data(symbol, start_date, end_date, response_content)
                    break
                except requests.exceptions.RequestException as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Request failed for {symbol} (attempt {attempt + 1}): {e}")
                    if attempt == 2:
                        raise
                    wait_time = (2 ** attempt) * 0.5
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Waiting {wait_time}s before retry")
                    time.sleep(wait_time)

            if not response_content:
                return []

            parse_start = time.time()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Parsing response for {symbol}")
            soup = BeautifulSoup(response_content, 'html.parser')
            table = soup.find('table')
            if not table:
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] No data found for {symbol}")
                return []

            # Process rows in batches
            batch_size = 100
            data = []
            rows = table.find_all('tr')[1:]  # Skip header row
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Found {len(rows)} rows for {symbol}")
            
            for i in range(0, len(rows), batch_size):
                batch_start = time.time()
                batch_rows = rows[i:i + batch_size]
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Processing batch {i//batch_size + 1} "
                      f"of {(len(rows) + batch_size - 1)//batch_size} for {symbol}")
                batch_data = self._process_rows(batch_rows, symbol)
                data.extend(batch_data)
                batch_duration = time.time() - batch_start
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Batch {i//batch_size + 1} for {symbol} "
                      f"processed in {batch_duration:.2f}s")

            if data:
                self._save_processed_data(symbol, start_date, end_date, data)
                self._save_to_csv(symbol, data)

            parse_duration = time.time() - parse_start
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Completed parsing {symbol} in {parse_duration:.2f}s - "
                  f"Found {len(data)} records")
            return data

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Error fetching data for {symbol}: {e}")
            return []

    def _process_rows(self, rows, symbol):
        """Process table rows into structured data"""
        batch_data = []
        for row in rows:
            try:
                cols = row.find_all('td')
                if cols:
                    row_data = {
                        'symbol': symbol,
                        'date': self.parse_date(cols[0].text.strip()),
                        'last_trade_price': self.parse_number(cols[1].text),
                        'max_price': self.parse_number(cols[2].text),
                        'min_price': self.parse_number(cols[3].text),
                        'avg_price': self.parse_number(cols[4].text),
                        'change_percentage': self.parse_number(cols[5].text),
                        'volume': self.parse_number(cols[6].text),
                        'turnover_best': self.parse_number(cols[7].text),
                        'total_turnover': self.parse_number(cols[8].text)
                    }
                    batch_data.append(row_data)
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Error processing row for {symbol}: {e}")
                continue
        return batch_data

    def _create_session(self):
        session = Session()
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def parse_date(self, date_str):
        """Parse date string to date object"""
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except:
            return None

    def parse_number(self, value):
        """Parse number strings to float"""
        try:
            clean_value = value.strip().replace(',', '').replace('%', '')
            if not clean_value:
                return 0.0
            return float(clean_value)
        except:
            return 0.0