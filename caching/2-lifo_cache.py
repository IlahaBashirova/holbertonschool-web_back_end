#!/usr/bin/env python3
""" LIFO Caching.
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache defines a caching systeem that follows the LIFO algoihm.
    """
    def __init__(self):
        """Initialize.
        """
        super().__init__()
    
    def put(self, key, item):
        """Add an item to dictionary.
        """
        if key is None or item is None:
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = list(self.cache_data.keys())[-1]
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
