from __future__ import with_statement
import os
import pickle
from typing import Final

CACHE_FILE: Final = "cache.p"

class Cache:
    data = {}
    def __init__(self):
        with open(CACHE_FILE, "rb") as fp:
            try:
                self.data = pickle.load(fp)
            except:
                pass

    def get(self, key: str):
        if key in self.data:
            return self.data[key]

    def set(self, key: str, value: any):
        self.data[key] = value

    def delete(self, key: str):
        del self.data[key]

    def close(self):
        with open(CACHE_FILE, "wb") as fp:
            pickle.dump(self.data, fp, protocol=pickle.HIGHEST_PROTOCOL)
