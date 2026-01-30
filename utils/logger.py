"""
Logger Module
Provides centralized logging functionality for the test framework
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from config.config import config


class Logger:
    """
    Custom Logger class for test framework.
    Provides formatted logging with file and console handlers.
    """
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str = __name__) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name (typically __name__ of the calling module)
            
        Returns:
            Configured logger instance
        """
        if name in Logger._loggers:
            return Logger._loggers[name]
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, config.log_level))
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # Create formatters
        log_format = config.get_logging_config()['format']
        date_format = config.get_logging_config()['datefmt']
        formatter = logging.Formatter(log_format, datefmt=date_format)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_dir = config.root_dir / 'reports'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'test_execution_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Store logger
        Logger._loggers[name] = logger
        
        return logger


# Create a default logger instance
logger = Logger.get_logger(__name__)
