-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- Create stock_data table
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    last_trade_price DOUBLE PRECISION,
    max_price DOUBLE PRECISION,
    min_price DOUBLE PRECISION,
    avg_price DOUBLE PRECISION,
    change_percentage DOUBLE PRECISION,
    volume INTEGER,
    turnover_best DOUBLE PRECISION,
    total_turnover DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_symbol_date UNIQUE (symbol, date)
);

-- Create index on stock_data
CREATE INDEX IF NOT EXISTS idx_symbol_date ON stock_data (symbol, date);

-- Create wishlist table
CREATE TABLE IF NOT EXISTS wishlist (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(255) UNIQUE NOT NULL
);