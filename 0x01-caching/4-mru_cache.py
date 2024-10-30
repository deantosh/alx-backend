#!/usr/bin/env python3
"""
Create a class MRUCache that inherits from BaseCaching and is a caching
system:
 - You must use self.cache_data - dictionary from the parent class BaseCaching
 - You can overload def __init__(self): but don’t forget to call the parent
   init: super().__init__()
 - def put(self, key, item):
   - Must assign to the dictionary self.cache_data the item value for the key.
   - If key or item is None, this method should not do anything.
   - If the number of items in self.cache_data is higher that
     BaseCaching.MAX_ITEMS:
     - you must discard the most recently used item (MRU algorithm)
     - you must print DISCARD: with the key discarded and following by a new
       line
 - def get(self, key):
   - Must return the value in self.cache_data linked to key.
   - If key is None or if the key doesn’t exist in self.cache_data, return
     None.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Defines caching system that uses MRU Algorithm
    """
    def __init__(self):
        """Initializes the class"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add items to cache"""
        if key is None or item is None:
            return

        # If key exists: update and move it to the end to mark as recently used
        if key in self.cache_data:
            self.cache_data[key] = item
            self.cache_data.move_to_end(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = next(reversed(self.cache_data))
            self.cache_data.pop(last_key)
            print(f"DISCARD: {last_key}")

        # Add new item to cache
        self.cache_data[key] = item

    def get(self, key):
        """Retrieves the data of a specified key"""
        if key is None:
            return None

        # check if key is found and move it to the end of cache
        if key in self.cache_data:
            self.cache_data.move_to_end(key)

        return self.cache_data.get(key)
