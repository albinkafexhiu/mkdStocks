import concurrent.futures
import time
from requests.sessions import Session
import queue
from threading import Semaphore, Thread
from datetime import datetime
import multiprocessing
import threading
import psutil
import requests

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
        
        # Increased concurrent requests
        self.request_semaphore = Semaphore(25)  # Further increased from 20 to 25
        self.last_request_time = {}
        self.min_request_interval = 0.02  # Further decreased from 0.03 to 0.02
        
        # Increased batch sizes
        self.batch_size = 10000
        self.save_queue = queue.Queue(maxsize=2000)
        
        # Initialize session with retry strategy
        self.session = Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))

    def wait_for_rate_limit(self, symbol):
        current_time = time.time()
        with self.request_semaphore:
            if symbol in self.last_request_time:
                elapsed = current_time - self.last_request_time[symbol]
                if elapsed < self.min_request_interval:
                    time.sleep(self.min_request_interval - elapsed)
            self.last_request_time[symbol] = time.time()

    def process_chunk(self, symbol, chunk, session):
        """Process a single date chunk"""
        try:
            self.wait_for_rate_limit(symbol)
            return self.data_fetcher.process(chunk, session)
        except Exception as e:
            print(f"Chunk processing error for {symbol}: {e}")
            return []

    @time_this(category='symbol_processing')
    def process_symbol(self, symbol):
        try:
            start_time = time.time()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting {symbol}")
            records = 0
            
            date_chunks = self.date_checker.process(symbol)
            if not date_chunks:
                return 0

            chunk_results = []
            # Create a dedicated thread pool for this symbol's chunks
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as chunk_executor:
                futures = [
                    chunk_executor.submit(self.process_chunk, symbol, chunk, self.session)
                    for chunk in date_chunks
                ]
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        chunk_data = future.result()
                        if chunk_data:
                            chunk_results.extend(chunk_data)
                            records += len(chunk_data)
                    except Exception as e:
                        print(f"Error processing chunk for {symbol}: {e}")

            if chunk_results:
                for i in range(0, len(chunk_results), self.batch_size):
                    batch = chunk_results[i:i + self.batch_size]
                    self.save_queue.put(batch)

            duration = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] {symbol}: {records} records in {duration:.2f}s")
            return records
            
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            return 0

    def batch_save_worker(self):
        """Worker thread for batch saving data"""
        batch = []
        timeout_count = 0
        max_timeouts = 3
        
        while timeout_count < max_timeouts:
            try:
                data = self.save_queue.get(timeout=10)
                timeout_count = 0  # Reset timeout counter on successful get
                
                if data is None:  # Shutdown signal
                    break
                
                batch.extend(data)
                
                # Process batch if it's full or queue is empty
                if len(batch) >= self.batch_size or (self.save_queue.empty() and batch):
                    self.db.save_stock_data(batch)
                    batch = []
                    
            except queue.Empty:
                timeout_count += 1
                if batch:  # Save any remaining data
                    self.db.save_stock_data(batch)
                    batch = []
            except Exception as e:
                print(f"Batch save error: {e}")
                if batch:  # Try to save what we can
                    try:
                        self.db.save_stock_data(batch)
                    except:
                        pass
                batch = []

    @time_this(category='total_execution', operation='pipeline_run')
    def run(self):
        try:
            run_start = time.time()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting pipeline...")
            symbols = self.symbol_scraper.process()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Found {len(symbols)} symbols")

            # Start the save worker thread
            save_worker = Thread(target=self.batch_save_worker, daemon=True)
            save_worker.start()

            # Calculate optimal number of workers
            cpu_count = multiprocessing.cpu_count()
            available_memory = psutil.virtual_memory().available
            max_workers = min(len(symbols), cpu_count * 4, 30)
            
            total_records = 0
            failed_symbols = []
            
            # Process symbols in batches to better manage resources
            symbol_batches = [symbols[i:i + max_workers] for i in range(0, len(symbols), max_workers)]
            
            for batch_idx, symbol_batch in enumerate(symbol_batches, 1):
                print(f"Processing batch {batch_idx}/{len(symbol_batches)}")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_symbol = {
                        executor.submit(self.process_symbol, symbol): symbol 
                        for symbol in symbol_batch
                    }
                    
                    for future in concurrent.futures.as_completed(future_to_symbol):
                        symbol = future_to_symbol[future]
                        try:
                            records = future.result()
                            total_records += records
                            if records == 0:
                                failed_symbols.append(symbol)
                        except Exception as e:
                            print(f"Failed {symbol}: {e}")
                            failed_symbols.append(symbol)

            # Signal save worker to finish and wait for completion
            self.save_queue.put(None)
            save_worker.join(timeout=30)

            total_duration = time.time() - run_start
            print(f"\n=== Pipeline Summary ===")
            print(f"Duration: {total_duration:.2f} seconds")
            print(f"Symbols processed: {len(symbols)} total, {len(symbols) - len(failed_symbols)} successful")
            print(f"Records: {total_records}")
            print(f"Speed: {total_records/total_duration:.2f} records/second")
            
            if failed_symbols:
                print(f"Failed symbols: {', '.join(failed_symbols)}")

            metrics.print_summary()
            return True

        except Exception as e:
            print(f"Pipeline error: {e}")
            return False

    def __del__(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()