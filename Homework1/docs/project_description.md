# Stock Market Analysis Project - MSE Data Pipeline

## Project Description

This project implements a data pipeline for the Macedonian Stock Exchange (MSE) using the Pipe and Filter architectural pattern. The system automates the collection, processing, and storage of historical stock market data for multiple companies listed on the MSE.

The pipeline consists of three main filters:
1. **Scraper Filter**: Retrieves stock symbols from MSE
2. **Date Checker Filter**: Determines the date ranges for data collection
3. **Data Processor Filter**: Fetches, processes, and stores the stock data

The system processes data for multiple companies (ADIN, ALK, GRNT, etc.) over a 10-year period, storing information such as daily trading prices, volumes, and turnovers. Data is stored in both a MySQL database (hosted on Aiven) and exported to CSV/Excel formats for further analysis.

Key features:
- Automated data collection from MSE website
- Efficient batch processing and database storage
- Data validation and cleaning
- Performance optimization with batch operations
- Export functionality to multiple formats
- Error handling and logging

The project is designed to be maintainable, scalable, and serves as a foundation for future stock market analysis applications.