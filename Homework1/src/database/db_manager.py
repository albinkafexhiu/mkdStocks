import os
from dotenv import load_dotenv
from sqlalchemy import UniqueConstraint, create_engine, text, MetaData, Table, Column, Integer, String, Date, Float, DateTime
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import time
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.engine = self._create_engine()
        self.metadata = MetaData()
        self.stock_data = self._create_table()

    def _create_engine(self):
        db_url = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            f"?sslmode={os.getenv('DB_SSL_MODE')}"
        )
        return create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=30,
            max_overflow=40,
            pool_timeout=30,
            pool_pre_ping=True,
            pool_recycle=3600
        )

    def _create_table(self):
        stock_data = Table(
            'stock_data',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('symbol', String(10), nullable=False),
            Column('date', Date, nullable=False),
            Column('last_trade_price', Float),
            Column('max_price', Float),
            Column('min_price', Float),
            Column('avg_price', Float),
            Column('change_percentage', Float),
            Column('volume', Integer),
            Column('turnover_best', Float),
            Column('total_turnover', Float),
            Column('created_at', DateTime, default=datetime.utcnow),
            UniqueConstraint('symbol', 'date', name='unique_symbol_date')
        )
        
        try:
            self.metadata.create_all(self.engine)
            with self.engine.connect() as conn:
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_symbol_date 
                    ON stock_data (symbol, date);
                """))
            print("Database table created successfully")
        except SQLAlchemyError as e:
            print(f"Error creating table: {e}")
        return stock_data

    def save_stock_data(self, data_rows):
        if not data_rows:
            return True

        # Prepare batch insert values
        values = []
        for row in data_rows:
            try:
                values.append({
                    'symbol': row['symbol'],
                    'date': row['date'],
                    'last_trade_price': float(str(row['last_trade_price']).replace(',', '')),
                    'max_price': float(str(row['max_price']).replace(',', '')),
                    'min_price': float(str(row['min_price']).replace(',', '')),
                    'avg_price': float(str(row['avg_price']).replace(',', '')),
                    'change_percentage': float(str(row['change_percentage']).replace(',', '')),
                    'volume': int(float(str(row['volume']).replace(',', ''))),
                    'turnover_best': float(str(row['turnover_best']).replace(',', '')),
                    'total_turnover': float(str(row['total_turnover']).replace(',', ''))
                })
            except (ValueError, TypeError) as e:
                print(f"Error processing row: {e}")
                continue

        if not values:
            return True

        # Use a simpler batch insert query
        query = text("""
            INSERT INTO stock_data (
                symbol, date, last_trade_price, max_price,
                min_price, avg_price, change_percentage,
                volume, turnover_best, total_turnover
            ) 
            VALUES (
                :symbol, :date, :last_trade_price, :max_price,
                :min_price, :avg_price, :change_percentage,
                :volume, :turnover_best, :total_turnover
            )
            ON CONFLICT (symbol, date) DO UPDATE SET
                last_trade_price = EXCLUDED.last_trade_price,
                max_price = EXCLUDED.max_price,
                min_price = EXCLUDED.min_price,
                avg_price = EXCLUDED.avg_price,
                change_percentage = EXCLUDED.change_percentage,
                volume = EXCLUDED.volume,
                turnover_best = EXCLUDED.turnover_best,
                total_turnover = EXCLUDED.total_turnover
        """)

        max_retries = 3
        retry_delay = 0.2

        for attempt in range(max_retries):
            try:
                with self.engine.begin() as connection:
                    connection.execute(query, values)
                print(f"Saved {len(values)} records to database")
                return True
            except SQLAlchemyError as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 1.5
                    continue
                print(f"Error saving to database: {e}")
                return False

    def get_last_date(self, symbol):
        try:
            with self.engine.connect() as connection:
                query = text("""
                    SELECT MAX(date) 
                    FROM stock_data 
                    WHERE symbol = :symbol
                """)
                result = connection.execute(query, {"symbol": symbol})
                return result.scalar()
        except SQLAlchemyError as e:
            print(f"Error getting last date: {e}")
            return None

    def test_connection(self):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return True
        except SQLAlchemyError as e:
            print(f"Database connection error: {e}")
            return False