"""Simple caching system for LLM responses and embeddings.

Implements in-memory cache with TTL and size limits.
"""

import time
import hashlib
import json
from typing import Any, Optional, Dict, Tuple
from collections import OrderedDict
from threading import Lock
from .logger import get_logger

logger = get_logger(__name__)


class Cache:
    """Simple LRU cache with TTL support."""
    
    def __init__(self, max_size: int = 100, default_ttl: int = 3600):
        """Initialize cache.
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time-to-live in seconds (1 hour default)
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
        self.lock = Lock()
        
        logger.info(f"Cache initialized: max_size={max_size}, ttl={default_ttl}s")
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Cache key string
        """
        # Create deterministic string from args
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        
        # Hash for shorter key
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self.lock:
            # Check if key exists
            if key not in self.cache:
                return None
            
            # Check if expired
            if key in self.timestamps:
                age = time.time() - self.timestamps[key]
                if age > self.default_ttl:
                    logger.debug(f"Cache expired: {key} (age: {age:.1f}s)")
                    del self.cache[key]
                    del self.timestamps[key]
                    return None
            
            # Move to end (LRU)
            self.cache.move_to_end(key)
            logger.debug(f"Cache hit: {key}")
            return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        with self.lock:
            # Remove oldest if at capacity
            if len(self.cache) >= self.max_size and key not in self.cache:
                oldest_key = next(iter(self.cache))
                logger.debug(f"Cache full, removing oldest: {oldest_key}")
                del self.cache[oldest_key]
                if oldest_key in self.timestamps:
                    del self.timestamps[oldest_key]
            
            # Add/update value
            self.cache[key] = value
            self.timestamps[key] = time.time()
            self.cache.move_to_end(key)
            
            logger.debug(f"Cache set: {key} (size: {len(self.cache)}/{self.max_size})")
    
    def delete(self, key: str):
        """Delete value from cache.
        
        Args:
            key: Cache key
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                if key in self.timestamps:
                    del self.timestamps[key]
                logger.debug(f"Cache deleted: {key}")
    
    def clear(self):
        """Clear all cache."""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
            logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        with self.lock:
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'usage_percent': (len(self.cache) / self.max_size * 100) if self.max_size > 0 else 0,
                'ttl': self.default_ttl
            }
    
    def cleanup_expired(self):
        """Remove expired entries."""
        with self.lock:
            now = time.time()
            expired_keys = [
                key for key, timestamp in self.timestamps.items()
                if now - timestamp > self.default_ttl
            ]
            
            for key in expired_keys:
                del self.cache[key]
                del self.timestamps[key]
            
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")


# Global caches for different purposes
_caches: Dict[str, Cache] = {}


def get_cache(name: str, max_size: int = 100, ttl: int = 3600) -> Cache:
    """Get or create named cache.
    
    Args:
        name: Cache name (e.g., 'llm_responses', 'embeddings')
        max_size: Maximum cache size
        ttl: Time-to-live in seconds
        
    Returns:
        Cache instance
        
    Example:
        >>> cache = get_cache('llm_responses', max_size=50, ttl=1800)
        >>> cache.set('key1', 'value1')
        >>> value = cache.get('key1')
    """
    if name not in _caches:
        _caches[name] = Cache(max_size, ttl)
    return _caches[name]


def cached_function(cache_name: str = 'default', ttl: int = 3600):
    """Decorator to cache function results.
    
    Args:
        cache_name: Name of cache to use
        ttl: Time-to-live for cached results
        
    Example:
        @cached_function(cache_name='api_calls', ttl=1800)
        def expensive_api_call(param1, param2):
            # Your expensive operation
            return result
    """
    def decorator(func):
        cache = get_cache(cache_name, ttl=ttl)
        
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = cache._generate_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                logger.debug(f"Using cached result for {func.__name__}")
                return result
            
            # Execute function
            logger.debug(f"Executing {func.__name__} (cache miss)")
            result = func(*args, **kwargs)
            
            # Cache result
            cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


def cache_llm_response(prompt: str, response: str, model: str = "default"):
    """Cache LLM response.
    
    Args:
        prompt: Input prompt
        response: LLM response
        model: Model name
    """
    cache = get_cache('llm_responses', max_size=50, ttl=3600)
    key = cache._generate_key(model, prompt)
    cache.set(key, response)
    logger.debug(f"Cached LLM response for model: {model}")


def get_cached_llm_response(prompt: str, model: str = "default") -> Optional[str]:
    """Get cached LLM response.
    
    Args:
        prompt: Input prompt
        model: Model name
        
    Returns:
        Cached response or None
    """
    cache = get_cache('llm_responses', max_size=50, ttl=3600)
    key = cache._generate_key(model, prompt)
    return cache.get(key)


def clear_all_caches():
    """Clear all caches."""
    for cache in _caches.values():
        cache.clear()
    logger.info("All caches cleared")


def get_all_cache_stats() -> Dict[str, Dict[str, Any]]:
    """Get statistics for all caches.
    
    Returns:
        Dictionary mapping cache names to their stats
    """
    return {
        name: cache.get_stats()
        for name, cache in _caches.items()
    }
