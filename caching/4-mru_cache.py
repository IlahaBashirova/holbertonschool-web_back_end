#!/usr/bin/env python3
""" MRU caching.
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU algorithm caching system.
    """
    def __init__(self):
        """Initialize.
        """
        super().__init__()
        self.order = []

    def _touch(self, key):
        """Create or update order list.
        """
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

    def put(self, key, item):
        """Add an item.
        """
        if key is None or item is None:
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key = self.order.pop(-1)
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")
        self.cache_data[key] = item
        self._touch(key)

    def get(self, key):
        """Get an item by key.
        """
        if key is None or key not in self.cache_data:
            return None
        self._touch(key)
        return self.cache_data.get(key)