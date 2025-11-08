#!/usr/bin/env python3
""" FIFO caching.
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache defines a caching system that follows the FIFO algorithm.
    """
    def __init__(self):
        """Initialize.
        """
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = list(self.cache_data.keys())[0]
            del self.cache_data[first_key]
            print(f"DISCARD: {first_key}")
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
