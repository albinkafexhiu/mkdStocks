import concurrent.futures
import time
from requests.sessions import Session
import queue
from threading import Semaphore
from datetime import datetime

from src.filters.symbol_scraper import SymbolScraperFilter
from src.filters.date_checker import DateCheckerFilter
from src.filters.data_fetcher import DataFetcherFilter
from src.database.db_manager import DatabaseManager
from src.utils.performance_metrics import metrics, time_this

class Pipeline:
    def __init__(self):
        self.symbol_scraper = SymbolScraperFilter()
        self.date_checker = DateCheckerFilter()
        self.data_fetcher = DataFetcherFilter()
        self.db = DatabaseManager()
        self.session = Session()
        self.request_semaphore = Semaphore(3)
        self.last_request_time = {}
        self.min_request_interval = 0.5

    def wait_for_rate_limit(self, symbol):
        """Implement rate limiting per symbol"""
        current_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Attempting to acquire semaphore for {symbol}")
        with self.request_semaphore:
            if symbol in self.last_request_time:
                elapsed = current_time - self.last_request_time[symbol]
                if elapsed < self.min_request_interval:
                    wait_time = self.min_request_interval - elapsed
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Rate limiting {symbol} - waiting {wait_time:.2f}s")
                    time.sleep(wait_time)
            self.last_request_time[symbol] = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Released semaphore for {symbol}")

    @time_this(category='symbol_processing')
    def process_symbol(self, symbol):
        try:
            start_time = time.time()
            print(f"\n[{datetime.now().strftime('%H:%M:%S.%f')}] Starting processing of {symbol}...")
            records = 0
            
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Checking dates for {symbol}")
            date_chunks = self.date_checker.process(symbol)
            if not date_chunks:
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Skipping {symbol} - no new data needed")
                return 0

            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Found {len(date_chunks)} date chunks for {symbol}")
            all_data = []
            for i, chunk in enumerate(date_chunks, 1):
                chunk_start = time.time()
                self.wait_for_rate_limit(symbol)
                print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Processing chunk {i}/{len(date_chunks)} for {symbol}: "
                      f"{chunk['start_date']} to {chunk['end_date']}")
                
                chunk_data = self.data_fetcher.process(chunk, self.session)
                chunk_duration = time.time() - chunk_start
                
                if chunk_data:
                    all_data.extend(chunk_data)
                    records += len(chunk_data)
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Chunk {i} for {symbol} completed in {chunk_duration:.2f}s - "
                          f"Got {len(chunk_data)} records")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Chunk {i} for {symbol} completed in {chunk_duration:.2f}s - "
                          f"No data found")

            # In Pipeline class, modify the relevant part:
                if all_data:
                    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Saving {len(all_data)} records for {symbol} to database")
                    batch_size = 2500  # Increased from 1000
                    for i in range(0, len(all_data), batch_size):
                        batch = all_data[i:i + batch_size]
                        self.db.save_stock_data(batch)

            total_duration = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Completed {symbol} in {total_duration:.2f}s - "
                  f"Total records: {records}")
            return records
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Error processing {symbol}: {e}")
            return 0

    @time_this(category='total_execution', operation='pipeline_run')
    def run(self):
        try:
            run_start = time.time()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting pipeline - fetching symbols...")
            symbols = self.symbol_scraper.process()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Found {len(symbols)} valid symbols")

            total_records = 0
            failed_symbols = []
            results_queue = queue.Queue()

            def process_symbol_with_queue(symbol):
                try:
                    records = self.process_symbol(symbol)
                    results_queue.put((symbol, records, None))
                except Exception as e:
                    results_queue.put((symbol, 0, str(e)))

            max_workers = min(10, len(symbols))
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting processing with {max_workers} workers")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(process_symbol_with_queue, symbol) 
                         for symbol in symbols]
                
                completed = 0
                while completed < len(symbols):
                    try:
                        symbol, records, error = results_queue.get(timeout=30)
                        completed += 1
                        if error:
                            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Failed {symbol}: {error}")
                            failed_symbols.append(symbol)
                        else:
                            total_records += records
                            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Queue processed {symbol}: {records} records "
                                  f"({completed}/{len(symbols)} symbols completed)")
                    except queue.Empty:
                        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Warning: No results received in the last 30 seconds")

            total_duration = time.time() - run_start
            print(f"\n[{datetime.now().strftime('%H:%M:%S.%f')}] Pipeline Execution Summary:")
            print(f"Total duration: {total_duration:.2f} seconds")
            print(f"Total symbols processed: {len(symbols)}")
            print(f"Successful symbols: {len(symbols) - len(failed_symbols)}")
            print(f"Failed symbols: {len(failed_symbols)}")
            if failed_symbols:
                print("Failed symbols list:", ", ".join(failed_symbols))
            print(f"Total records: {total_records}")
            print(f"Average time per symbol: {total_duration/len(symbols):.2f} seconds")
            
            metrics.print_summary()
            return True

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Pipeline error: {e}")
            return False

    def __del__(self):
        if self.session:
            self.session.close()