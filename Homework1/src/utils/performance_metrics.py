import time
import psutil
import threading
from functools import wraps
from datetime import datetime
from typing import Dict, List, Any

class PerformanceMetrics:
    def __init__(self):
        self.metrics: Dict[str, List[Dict[str, Any]]] = {
            'symbol_processing': [],
            'database_operations': [],
            'network_requests': [],
            'total_execution': []
        }
        self._lock = threading.Lock()

    def record_metric(self, category: str, operation: str, duration: float, 
                     success: bool, additional_info: Dict = None):
        """Record a performance metric with thread-safe operation."""
        metric = {
            'timestamp': datetime.now(),
            'operation': operation,
            'duration': duration,
            'success': success,
            'memory_usage': psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            'additional_info': additional_info or {}
        }
        
        with self._lock:
            if category not in self.metrics:
                self.metrics[category] = []
            self.metrics[category].append(metric)

    def get_summary(self) -> Dict:
        """Generate a summary of all recorded metrics."""
        summary = {}
        
        for category, measurements in self.metrics.items():
            if not measurements:
                continue
                
            durations = [m['duration'] for m in measurements]
            success_count = sum(1 for m in measurements if m['success'])
            
            summary[category] = {
                'total_operations': len(measurements),
                'successful_operations': success_count,
                'failure_rate': (len(measurements) - success_count) / len(measurements),
                'average_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations),
                'total_duration': sum(durations),
                'average_memory_mb': sum(m['memory_usage'] for m in measurements) / len(measurements)
            }
            
        return summary

    def print_summary(self):
        """Print a formatted summary of all metrics."""
        summary = self.get_summary()
        
        print("\n=== Performance Metrics Summary ===")
        for category, stats in summary.items():
            print(f"\n{category.upper()}")
            print(f"Total Operations: {stats['total_operations']}")
            print(f"Success Rate: {((1 - stats['failure_rate']) * 100):.2f}%")
            print(f"Average Duration: {stats['average_duration']:.2f}s")
            print(f"Min/Max Duration: {stats['min_duration']:.2f}s / {stats['max_duration']:.2f}s")
            print(f"Total Duration: {stats['total_duration']:.2f}s")
            print(f"Average Memory Usage: {stats['average_memory_mb']:.2f}MB")

# Global metrics instance
metrics = PerformanceMetrics()

def time_this(category: str, operation: str = None):
    """Decorator to time and record metrics for any function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = False
            try:
                result = func(*args, **kwargs)
                success = True
                return result
            finally:
                duration = time.time() - start_time
                op_name = operation or func.__name__
                metrics.record_metric(
                    category=category,
                    operation=op_name,
                    duration=duration,
                    success=success
                )
        return wrapper
    return decorator