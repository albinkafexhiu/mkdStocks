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

## Homework 2
*To be implemented*

## Homework 3
*To be implemented*

## Homework 4
*To be implemented*