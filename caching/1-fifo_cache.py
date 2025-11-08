#!/usr/bin/python3
""" FIFO caching.
"""
from base_caching import BaseCaching


def __init__(self):
    """Initialize
    """
    super().__init__()

def put(self, key, item):
    """Add an item in the cache.
    """
    if key is None or item is None:
        return 
    if len(self.cache_data)>=BaseCaching.MAX_ITEMS:
        discarder_item=self.cache_data.popitem(last=False)
        print("DISCARD: ", f"{discarder_item[0]}")
    self.cache_data[key]=item
    
def get(self, key):
    """Get an item by key.
    """
    if key is None or key not in self.cache_data:
        return None
    return self.cache_data.get(key)


    