# backend/data_fetcher/cache_manager.py
from cachetools import TTLCache
import hashlib
import json
from typing import Any, Optional
from config import Config

class CacheManager:
    """Manage caching of API responses"""
    
    def __init__(self, maxsize: int = 1000, ttl: int = None):
        """
        Initialize cache manager
        
        Args:
            maxsize: Maximum number of items in cache
            ttl: Time to live in seconds (default from config)
        """
        self.ttl = ttl or Config.CACHE_DURATION
        self.cache = TTLCache(maxsize=maxsize, ttl=self.ttl)
    
    @staticmethod
    def _generate_key(prefix: str, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = json.dumps(kwargs, sort_keys=True)
        hash_obj = hashlib.md5(key_data.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    
    def get(self, prefix: str, **kwargs) -> Optional[Any]:
        """Get item from cache"""
        key = self._generate_key(prefix, **kwargs)
        return self.cache.get(key)
    
    def set(self, prefix: str, value: Any, **kwargs):
        """Set item in cache"""
        key = self._generate_key(prefix, **kwargs)
        self.cache[key] = value
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'maxsize': self.cache.maxsize,
            'ttl': self.ttl,
            'currsize': self.cache.currsize
        }