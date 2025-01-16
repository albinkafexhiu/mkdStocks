from src.core.pipeline import Pipeline
import time

def main():
    start_time = time.time()
    print("Starting stock market data collection...")
    
    pipeline = Pipeline()
    success = pipeline.run()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nExecution completed in {duration:.2f} seconds")
    print(f"Status: {'Success' if success else 'Failed'}")

if __name__ == "__main__":
    main()