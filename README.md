# Macedonian Stock Exchange Analysis

## Team Members
- Albin Kafexhiu (211515)
- Ajla Zenuni (223199)

## Homework 1: Data Pipeline Implementation

### Overview
Implementation of a data pipeline using Pipe and Filter architecture to collect and process historical stock market data from the Macedonian Stock Exchange.

### Implementation Details
- **Architecture**: Pipe and Filter pattern for data processing
- **Data Storage**: PostgreSQL database + CSV files
- **Programming Language**: Python

### Filters
1. **Symbol Scraper Filter**
   - Automatically retrieves all issuers from MSE
   - Excludes bonds and numerical codes
   - Handles input validation

2. **Date Checker Filter**
   - Verifies last available date for each issuer
   - Determines required data range (10 years)
   - Creates optimized date chunks for processing

3. **Data Fetcher Filter**
   - Retrieves historical data for each symbol
   - Implements rate limiting and error handling
   - Handles data formatting and validation

### Data Storage
- Raw data stored in HTML format
- Processed data saved in both CSV and database
- Proper data formatting with regional number formats

### Performance Results
- Total Duration: 261.85 seconds
- Symbols Processed: 141/141 successful
- Total Records: 294521
- Average Processing Time: 1.86 seconds per symbol
- Total Operations: 141 (100% Success Rate)
- Processing Time Range: 5.15s - 27.56s
- Average Memory Usage: 111.14MB

## Homework 2: Web Application Development

### Overview
Development of a web application for visualizing and analyzing Macedonian Stock Exchange data using modern web technologies and a microservices architecture.

### Implementation Details
- **Frontend**: React (Vite) + TypeScript + Tailwind CSS
- **Backend**: FastAPI + PostgreSQL
- **Architecture**: Microservices architecture with RESTful APIs

### Key Features
1. **Authentication System**
   - User registration and login
   - Secure password handling
   - Session management

2. **Stock Data Visualization**
   - Interactive line charts using Recharts
   - Historical price viewing
   - Volume and turnover analysis
   - Responsive data tables

3. **Market Overview Dashboard**
   - Monthly top gainers and losers
   - Volume leaders visualization
   - Market statistics summary
   - Trading activity metrics

### Technical Stack
- **Frontend Libraries**:
  - Recharts for data visualization
  - Lucide icons for UI elements
  - Tailwind CSS for styling
  - TypeScript for type safety

- **Backend Features**:
  - RESTful API endpoints
  - Database integration
  - Data aggregation services
  - Error handling and validation

### Project Demo
Watch our technical prototype demonstration: [YouTube Demo](https://youtu.be/RJ8Wc3pdDs8)

### Current Progress
- Implemented user authentication
- Created responsive navigation system
- Developed stock data visualization components
- Built market overview dashboard
- Integrated backend APIs with frontend

## Homework 3: Stock Market Analysis Tools

### Homework3 Demo
Watch our technical prototype demonstration: [YouTube Demo](https://youtu.be/WJCrvPGr7b4)

### Overview
Implementation of comprehensive analysis tools for the Macedonian Stock Exchange, providing technical, fundamental, and predictive analysis capabilities.

### Technical Analysis (Completed)
Implementation of technical analysis tools that process historical stock data to identify trading signals.

#### Features
1. **Technical Indicators**
   - 5 Oscillators (RSI, Stochastic K/D, Williams %R, CCI, MFI)
   - 5 Moving Averages (SMA, EMA, WMA, TEMA, WEMA)
   - Multi-timeframe analysis (daily/weekly/monthly)

2. **Visualization**
   - Interactive price and indicator charts
   - Customizable timeframe selection
   - Real-time signal generation

#### Implementation Details
- **Backend**: FastAPI + pandas + ta library
- **Frontend**: React + Recharts
- **Data Processing**: Automated indicator calculations
- **Performance**: Optimized for real-time analysis

### Fundamental Analysis (Completed)
Implementation of news-based sentiment analysis for market trend prediction using Natural Language Processing.

#### Features
1. **News Scraping System**
   - Automated scraping from major Macedonian financial news sources
   - Multi-source integration (Kapital.mk, BiznisInfo.mk)
   - Efficient content extraction and processing
   - Rate-limited requests with retry mechanisms

2. **Sentiment Analysis Engine**
   - Machine translation (Macedonian to English) using MarianMT
   - Financial-specific sentiment analysis using FinBERT
   - Sentiment score calculation and trading signal generation
   - Market-wide sentiment aggregation

3. **Data Processing Pipeline**
   - Automated news collection and processing
   - Real-time sentiment analysis
   - Historical sentiment tracking
   - Company-specific and market-wide analysis

### LSTM Price Prediction
*To be implemented*


## Homework 4: Design Patterns and Microservices

### Design Patterns Implementation

#### 1. Technical Analysis Refactoring
Started refactoring the technical analysis component using the Strategy Pattern combined with Factory Pattern for better code organization and maintainability. The implementation includes:

- Strategy Pattern for technical indicators (oscillators and moving averages)
- Factory Pattern for indicator creation and management
- Organized code structure under `app/services/technical/`
- Maintained all existing functionality while improving code quality
- Enhanced extensibility for adding new technical indicators

#### 2. News Analysis System
Refactored the news and sentiment analysis system using Template Method and Chain of Responsibility patterns. The implementation includes:

- Template Method Pattern for standardizing news scraping from different sources
- Chain of Responsibility for processing pipeline (scraping → translation → sentiment analysis)
- Organized modular structure under `app/services/news/`
- Improved error handling and maintainability
- Simplified process of adding new news sources or processing steps

#### 3. Stock Data Processing
Implemented Repository and Builder patterns for stock data processing to improve code organization and maintainability. The implementation includes:

- Repository Pattern for abstracting database operations
- Builder Pattern for constructing complex market data responses
- Organized modular structure under `app/services/stocks/`
- Enhanced error handling and data validation
- Simplified process of adding new data processing features

### Frontend Architecture Improvements
Refactored the frontend components using modern React patterns and best practices for better maintainability and reusability:

- Implemented custom hooks for data management and shared logic (useStockData, useAnalysis, useFundamental, useSymbols)
- Created reusable UI components with TypeScript for better type safety
- Applied component composition pattern for complex UI elements
- Organized code structure by feature domains (analysis, stocks, fundamental)
- Improved error handling and loading states across all components
- Standardized symbol selection and data visualization components
- Enhanced code maintainability through proper separation of concerns
- Implemented proper TypeScript interfaces for all data structures
- Created consistent UI patterns across different sections of the application

The frontend refactoring focuses on making the code more maintainable, reusable, and type-safe while maintaining all existing functionality and improving user experience.

*More implementations coming soon...*