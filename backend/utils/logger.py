"""Centralized logging system for Meeting Analyzer Pro.

Provides consistent logging across all modules with rotation and formatting.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional


class AppLogger:
    """Application logger with file and console output."""
    
    _instance: Optional['AppLogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Singleton pattern to ensure one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger with file and console handlers."""
        if self._initialized:
            return
        
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("MeetingAnalyzer")
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # File handler with rotation (10MB max, keep 5 files)
        log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self._initialized = True
        self.logger.info("=" * 80)
        self.logger.info("Meeting Analyzer Pro - Logger Initialized")
        self.logger.info("=" * 80)
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """Get logger instance with optional name.
        
        Args:
            name: Optional module name for logger
            
        Returns:
            Logger instance
        """
        if name:
            return logging.getLogger(f"MeetingAnalyzer.{name}")
        return self.logger
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, exc_info: bool = False, **kwargs):
        """Log error message with optional exception info."""
        self.logger.error(message, exc_info=exc_info, **kwargs)
    
    def critical(self, message: str, exc_info: bool = True, **kwargs):
        """Log critical message with exception info."""
        self.logger.critical(message, exc_info=exc_info, **kwargs)
    
    def log_function_call(self, func_name: str, **params):
        """Log function call with parameters."""
        param_str = ", ".join(f"{k}={v}" for k, v in params.items())
        self.logger.debug(f"Calling {func_name}({param_str})")
    
    def log_api_call(self, provider: str, model: str, tokens: int = None):
        """Log API call details."""
        msg = f"API Call: {provider}/{model}"
        if tokens:
            msg += f" | Tokens: {tokens}"
        self.logger.info(msg)
    
    def log_error_with_context(self, error: Exception, context: dict):
        """Log error with additional context."""
        self.logger.error(
            f"Error: {type(error).__name__}: {str(error)}",
            extra={"context": context},
            exc_info=True
        )


# Global logger instance
_app_logger = AppLogger()


def get_logger(name: str = None) -> logging.Logger:
    """Get logger instance.
    
    Args:
        name: Optional module name
        
    Returns:
        Logger instance
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return _app_logger.get_logger(name)


def log_function_call(func_name: str, **params):
    """Log function call with parameters.
    
    Example:
        >>> log_function_call("process_file", file="test.txt", type="meeting")
    """
    _app_logger.log_function_call(func_name, **params)


def log_api_call(provider: str, model: str, tokens: int = None):
    """Log API call details.
    
    Example:
        >>> log_api_call("gemini", "gemini-2.5-flash", tokens=1500)
    """
    _app_logger.log_api_call(provider, model, tokens)


def log_error(error: Exception, context: dict = None):
    """Log error with optional context.
    
    Example:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     log_error(e, {"file": "test.txt", "user": "admin"})
    """
    if context:
        _app_logger.log_error_with_context(error, context)
    else:
        _app_logger.error(str(error), exc_info=True)
