"""
Performance Monitoring Utility
Tracks and reports performance metrics for test execution
"""
import time
import psutil
from typing import Dict, List, Optional
from datetime import datetime
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class PerformanceMonitor:
    """Monitor and track performance metrics during test execution."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.metrics: List[Dict] = []
        self.start_time: Optional[float] = None
        self.page_load_times: List[float] = []
        
    def start_monitoring(self) -> None:
        """Start performance monitoring."""
        self.start_time = time.time()
        logger.info("Performance monitoring started")
        
    def stop_monitoring(self) -> Dict:
        """
        Stop monitoring and return metrics.
        
        Returns:
            Dictionary containing performance metrics
        """
        if not self.start_time:
            logger.warning("Monitoring was not started")
            return {}
            
        duration = time.time() - self.start_time
        
        metrics = {
            'total_duration': round(duration, 2),
            'average_page_load': self._calculate_average_page_load(),
            'memory_usage': self._get_memory_usage(),
            'cpu_usage': self._get_cpu_usage(),
            'timestamp': datetime.now().isoformat()
        }
        
        self.metrics.append(metrics)
        logger.info(f"Performance metrics: {metrics}")
        return metrics
        
    def record_page_load(self, load_time: float) -> None:
        """
        Record page load time.
        
        Args:
            load_time: Page load time in seconds
        """
        self.page_load_times.append(load_time)
        logger.debug(f"Page load time recorded: {load_time}s")
        
    def _calculate_average_page_load(self) -> float:
        """Calculate average page load time."""
        if not self.page_load_times:
            return 0.0
        return round(sum(self.page_load_times) / len(self.page_load_times), 2)
        
    def _get_memory_usage(self) -> Dict:
        """Get current memory usage."""
        memory = psutil.virtual_memory()
        return {
            'total_mb': round(memory.total / (1024 * 1024), 2),
            'used_mb': round(memory.used / (1024 * 1024), 2),
            'percent': memory.percent
        }
        
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)
        
    def get_all_metrics(self) -> List[Dict]:
        """
        Get all recorded metrics.
        
        Returns:
            List of all performance metrics
        """
        return self.metrics
        
    def clear_metrics(self) -> None:
        """Clear all recorded metrics."""
        self.metrics = []
        self.page_load_times = []
        self.start_time = None
        logger.info("Performance metrics cleared")


# Global performance monitor instance
performance_monitor = PerformanceMonitor()
