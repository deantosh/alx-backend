#!/usr/bin/env python3
"""
Create a class LFUCache that inherits from BaseCaching and is a caching
system:
 - You must use self.cache_data - dictionary from the parent class BaseCaching
 - You can overload def __init__(self): but don’t forget to call the parent
   init: super().__init__()
 - def put(self, key, item):
   - Must assign to the dictionary self.cache_data the item value for the key.
   - If key or item is None, this method should not do anything.
   - If the number of items in self.cache_data is higher that
     BaseCaching.MAX_ITEMS:
     - you must discard the least frequency used item (LFU algorithm)
     - if you find more than 1 item to discard, you must use the LRU
       algorithm to discard only the least recently used
     - you must print DISCARD: with the key discarded and following by a new
       line
 - def get(self, key):
   - Must return the value in self.cache_data linked to key.
   - If key is None or if the key doesn’t exist in self.cache_data, return
     None.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Defines caching system that uses LFU Algorithm
    """
    def __init__(self):
        """Initializes the class"""
        super().__init__()
        self.cache_data = OrderedDict()
        self.key_freq = {}
        self.min_freq = 0

    def put(self, key, item):
        """Add items to cache"""
        if key is None or item is None:
            return

        # If key exists: update and move it to the end to mark as recently used
        if key in self.cache_data:
            self.key_freq[key] += 1
            self.cache_data[key] = item
            self.cache_data.move_to_end(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # check keys with minimum frequency
            list_keys_min_freq = [
                k for k, v in self.key_freq.items() if v == self.min_freq]

            # Case: only one key found
            if len(list_keys_min_freq) == 0:
                discarded_key = list_keys_min_freq[0]
            else:
                discarded_key = list_keys_min_freq[0]  # Multiple keys found

            # Print and discard key
            self.cache_data.pop(discarded_key)
            self.key_freq.pop(discarded_key)
            print(f"DISCARD: {discarded_key}")

        # Add new item to cache
        self.cache_data[key] = item
        self.key_freq[key] = 1
        self.cache_data.move_to_end(key)

        # Update value of minimm frequency after using key
        self.min_freq = min(self.key_freq.values())

    def get(self, key):
        """Retrieves the data of a specified key"""
        if key is None:
            return None

        # check if key is found and move it to the end of cache
        if key in self.cache_data:
            self.key_freq[key] += 1
            self.cache_data.move_to_end(key)

        # Update value of minimm frequency after using key
        self.min_freq = min(self.key_freq.values())

        return self.cache_data.get(key)
