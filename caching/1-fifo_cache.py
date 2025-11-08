#!/usr/bin/env python3
"""FIFOCache module.
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache defines a caching system that follows the FIFO algorithm."""
    
    def __init__(self):
        """Initialize the cache."""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache."""
        if key is None or item is None:
            return

        # If key already exists, just update the value (no eviction)
        if key in self.cache_data:
            self.cache_data[key] = item
            return

        # If cache is full, remove the first inserted item (FIFO)
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discarder_key, _ = self.cache_data.popitem(last=False)
            print("DISCARD: {}".format(discarder_key))

        # Finally, store the new item
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key."""
        if key is None:
            return None
        return self.cache_data.get(key)
