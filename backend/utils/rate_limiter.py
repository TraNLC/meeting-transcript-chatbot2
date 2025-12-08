"""Rate limiting for API calls to prevent quota exhaustion.

Implements token bucket algorithm for rate limiting.
"""

import time
from typing import Dict, Optional
from datetime import datetime, timedelta
from threading import Lock
from .logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Rate limiter using token bucket algorithm."""
    
    def __init__(self, max_calls: int, time_window: int):
        """Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
            
        Example:
            >>> limiter = RateLimiter(max_calls=15, time_window=60)  # 15 calls per minute
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: Dict[str, list] = {}
        self.lock = Lock()
        
        logger.info(f"RateLimiter initialized: {max_calls} calls per {time_window}s")
    
    def is_allowed(self, key: str = "default") -> bool:
        """Check if call is allowed.
        
        Args:
            key: Identifier for rate limiting (e.g., user_id, api_key)
            
        Returns:
            True if call is allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            
            # Initialize if first call
            if key not in self.calls:
                self.calls[key] = []
            
            # Remove old calls outside time window
            self.calls[key] = [
                call_time for call_time in self.calls[key]
                if now - call_time < self.time_window
            ]
            
            # Check if limit reached
            if len(self.calls[key]) >= self.max_calls:
                oldest_call = self.calls[key][0]
                wait_time = self.time_window - (now - oldest_call)
                logger.warning(
                    f"Rate limit reached for '{key}'. "
                    f"Wait {wait_time:.1f}s before next call."
                )
                return False
            
            # Add current call
            self.calls[key].append(now)
            return True
    
    def wait_if_needed(self, key: str = "default", max_wait: int = 60) -> bool:
        """Wait if rate limit reached.
        
        Args:
            key: Identifier for rate limiting
            max_wait: Maximum time to wait in seconds
            
        Returns:
            True if call can proceed, False if max_wait exceeded
        """
        if self.is_allowed(key):
            return True
        
        with self.lock:
            now = time.time()
            if key in self.calls and self.calls[key]:
                oldest_call = self.calls[key][0]
                wait_time = self.time_window - (now - oldest_call)
                
                if wait_time > max_wait:
                    logger.error(f"Wait time ({wait_time:.1f}s) exceeds max_wait ({max_wait}s)")
                    return False
                
                logger.info(f"Waiting {wait_time:.1f}s for rate limit...")
                time.sleep(wait_time + 0.1)  # Add small buffer
                return True
        
        return False
    
    def get_remaining_calls(self, key: str = "default") -> int:
        """Get number of remaining calls in current window.
        
        Args:
            key: Identifier for rate limiting
            
        Returns:
            Number of remaining calls
        """
        with self.lock:
            if key not in self.calls:
                return self.max_calls
            
            now = time.time()
            recent_calls = [
                call_time for call_time in self.calls[key]
                if now - call_time < self.time_window
            ]
            
            return max(0, self.max_calls - len(recent_calls))
    
    def get_reset_time(self, key: str = "default") -> Optional[datetime]:
        """Get time when rate limit resets.
        
        Args:
            key: Identifier for rate limiting
            
        Returns:
            Datetime when limit resets, or None if no calls made
        """
        with self.lock:
            if key not in self.calls or not self.calls[key]:
                return None
            
            oldest_call = self.calls[key][0]
            reset_time = datetime.fromtimestamp(oldest_call + self.time_window)
            return reset_time
    
    def reset(self, key: str = None):
        """Reset rate limiter for specific key or all keys.
        
        Args:
            key: Identifier to reset, or None to reset all
        """
        with self.lock:
            if key:
                if key in self.calls:
                    self.calls[key] = []
                    logger.info(f"Rate limiter reset for key: {key}")
            else:
                self.calls = {}
                logger.info("Rate limiter reset for all keys")


# Global rate limiters for different services
_rate_limiters: Dict[str, RateLimiter] = {}


def get_rate_limiter(service: str, max_calls: int = 15, time_window: int = 60) -> RateLimiter:
    """Get or create rate limiter for service.
    
    Args:
        service: Service name (e.g., 'gemini', 'openai')
        max_calls: Maximum calls per time window
        time_window: Time window in seconds
        
    Returns:
        RateLimiter instance
        
    Example:
        >>> limiter = get_rate_limiter('gemini', max_calls=15, time_window=60)
        >>> if limiter.is_allowed():
        ...     make_api_call()
    """
    if service not in _rate_limiters:
        _rate_limiters[service] = RateLimiter(max_calls, time_window)
    return _rate_limiters[service]


def check_rate_limit(service: str, key: str = "default") -> bool:
    """Check if API call is allowed.
    
    Args:
        service: Service name
        key: Identifier for rate limiting
        
    Returns:
        True if allowed, False otherwise
    """
    limiter = get_rate_limiter(service)
    return limiter.is_allowed(key)


def wait_for_rate_limit(service: str, key: str = "default", max_wait: int = 60) -> bool:
    """Wait for rate limit if needed.
    
    Args:
        service: Service name
        key: Identifier for rate limiting
        max_wait: Maximum wait time in seconds
        
    Returns:
        True if can proceed, False if max_wait exceeded
    """
    limiter = get_rate_limiter(service)
    return limiter.wait_if_needed(key, max_wait)
