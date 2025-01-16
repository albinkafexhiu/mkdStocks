from datetime import datetime, timedelta
import math

from src.database.db_manager import DatabaseManager 
class DateCheckerFilter:
    def __init__(self):
        self.db = DatabaseManager()
        self.chunk_size = timedelta(days=365)

    def process(self, symbol):
        try:
            current_date = datetime.now().date()
            ten_years_ago = current_date.replace(year=current_date.year - 10)
            
            # Check last date in database
            last_date = self.db.get_last_date(symbol)
            
            if last_date is None:
                start_date = ten_years_ago
            else:
                start_date = last_date + timedelta(days=1)
                
            if start_date >= current_date:
                return None  # No new data needed
                
            # Calculate date chunks
            date_chunks = []
            chunk_start = start_date
            
            while chunk_start < current_date:
                chunk_end = min(chunk_start + self.chunk_size, current_date)
                date_chunks.append({
                    'symbol': symbol,
                    'start_date': chunk_start,
                    'end_date': chunk_end
                })
                chunk_start = chunk_end + timedelta(days=1)
            
            return date_chunks
                
        except Exception as e:
            print(f"Error checking dates for {symbol}: {e}")
            return None