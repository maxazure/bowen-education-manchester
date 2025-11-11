"""
Simple TTL-based caching decorator for database queries

This module provides caching decorators for functions that accept
database sessions as parameters. The cache key is based on function
arguments (excluding the db session) and has a time-to-live (TTL).
"""

import functools
import time
from typing import Any, Callable, Dict, Tuple


class TTLCache:
    """Simple time-to-live cache"""

    def __init__(self, ttl: int = 300):
        """
        Initialize cache

        Args:
            ttl: Time-to-live in seconds (default: 5 minutes)
        """
        self.ttl = ttl
        self.cache: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Any:
        """Get value from cache if not expired"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                # Expired, remove from cache
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp"""
        self.cache[key] = (value, time.time())

    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()

    def invalidate(self, pattern: str = None) -> None:
        """
        Invalidate cache entries

        Args:
            pattern: If provided, only invalidate keys containing this pattern
        """
        if pattern is None:
            self.clear()
        else:
            keys_to_delete = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.cache[key]


# Global cache instances
_navigation_cache = TTLCache(ttl=600)  # 10 minutes for navigation
_content_cache = TTLCache(ttl=300)  # 5 minutes for content lists
_settings_cache = TTLCache(ttl=600)  # 10 minutes for settings


def cache_query(
    cache_instance: TTLCache, exclude_params: Tuple[str, ...] = ("db",)
) -> Callable:
    """
    Decorator to cache query results with TTL

    Args:
        cache_instance: Cache instance to use
        exclude_params: Parameter names to exclude from cache key (default: ('db',))

    Returns:
        Decorated function with caching
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key from function name and arguments (excluding db)
            # Get function signature
            import inspect

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Build cache key from non-excluded parameters
            cache_key_parts = [func.__name__]
            for param_name, param_value in bound_args.arguments.items():
                if param_name not in exclude_params:
                    cache_key_parts.append(f"{param_name}={param_value}")

            cache_key = "|".join(cache_key_parts)

            # Try to get from cache
            cached_result = cache_instance.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_instance.set(cache_key, result)
            return result

        # Add cache control methods to the wrapper
        wrapper.clear_cache = cache_instance.clear
        wrapper.invalidate_cache = cache_instance.invalidate

        return wrapper

    return decorator


# Convenience decorators for different cache types
def cache_navigation(func: Callable) -> Callable:
    """Cache navigation queries (10 min TTL)"""
    return cache_query(_navigation_cache)(func)


def cache_content(func: Callable) -> Callable:
    """Cache content list queries (5 min TTL)"""
    return cache_query(_content_cache)(func)


def cache_settings(func: Callable) -> Callable:
    """Cache site settings queries (10 min TTL)"""
    return cache_query(_settings_cache)(func)


def clear_all_caches():
    """Clear all caches"""
    _navigation_cache.clear()
    _content_cache.clear()
    _settings_cache.clear()
