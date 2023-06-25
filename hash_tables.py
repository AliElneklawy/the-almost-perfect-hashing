from struct import pack

class HashTable:
    def __init__(self):
        self.max = 100
        self.arr = [[] for _ in range(self.max)]
        self.occupied = 0
    
    def fnv_hash(self, key):
        if isinstance(key, str):
            key = str(key)
            hash = 0
            for char in key:
                hash += ord(char)
        elif isinstance(key, float):
            hash_bytes = pack('!d', key)
            hash_int = int.from_bytes(hash_bytes, byteorder='big')
            hash = hash_int
        else:
            hash = key

        FNV_PRIME = 16777619
        FNV_OFFSET_BASIS = 2166136261

        hash_value = FNV_OFFSET_BASIS
        while hash != 0:
            hash_value ^= hash & 0xFF
            hash_value *= FNV_PRIME
            hash >>= 8

        return hash_value % self.max
    
    def __setitem__(self, key, val):
        self.occupied += 1
        h = self.fnv_hash(key)
        found = False

        for idx, elmnt in enumerate(self.arr[h]): #separate chaining method
            if len(elmnt) == 2 and elmnt[0] == key:
                found = True
                self.arr[h][idx] = (key, val)
                break
        
        if not found:
            self.arr[h].append((key, val))
        
    def __getitem__(self, key):
         h = self.fnv_hash(key)
         for elmnt in self.arr[h]:
             if elmnt[0] == key:
                 return elmnt[1]
             
    def __delitem__(self, key):
        self.occupied -= 1
        h = self.fnv_hash(key)
        for idx, elmnt in enumerate(self.arr[h]):
            if elmnt[0] == key:
                del self.arr[h][idx]
