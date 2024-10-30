from hash_table import HashSet, HashMap, Bucket
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        new_size = get_next_size()

        # storing all the keys to be rehashed in a list 
        elements = []
        for item in self.hash_set:
            if item is not None:
                if isinstance(item, Bucket): # for chaining part
                    elements.extend(item.b_list)

                else: # for linear and double
                    elements.append(item)

        # resizing the hashset
        self.hash_set_size = new_size
        self.hash_set = new_size * [None]
        self._n = 0

        #inserting all the keys back in the bigger hash_set
        for key in elements:
            self.insert(key)
                
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        new_size = get_next_size()

        elements = []
        for item in self.hash_map:
            if item is not None:
                if isinstance(item, Bucket): # for chaining part
                    elements.extend(item.b_list)

                else: # for linear and double
                    elements.append(item)

        self.hash_map_size = new_size
        self.hash_map = new_size * [None]
        self._n = 0

        for x in elements:
            self.insert(x)

        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()