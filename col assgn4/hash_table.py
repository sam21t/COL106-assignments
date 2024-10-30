from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        self.params = params
    
    def insert(self, x):
        pass
    
    def find(self, key):
        pass
    
    def get_slot(self, key):
        pass
    
    def get_load(self):
        pass
    
    def __str__(self):
        pass

    def poly_accu_hash(self,s,z):
        #values to letters
        def p(char):
            if 'a'<=char<='z':
                return ord(char) - ord('a')
            elif 'A'<=char<='Z':
                return ord(char) - ord('A') + 26
            
        hash_value = 0
        n = len(s)

        for i in range(n):
            hash_value += p(s[i]) * (z ** i)

        return hash_value
    
    def h1(self,s,z1,table_size):
        return self.poly_accu_hash(s,z1) % table_size
    
    def h2(self,s,z2,c2):
        return (c2 - (self.poly_accu_hash(s,z2) % c2)) 

    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
        self.hash_set_size = self.params[-1]
        self.hash_set = self.hash_set_size*[None]
        self._n = 0 #no of elements
    
    def insert(self, key):
        initial_index = self.h1(key, self.params[0],self.hash_set_size)

        if self.collision_type == 'Chain':
            if self.hash_set[initial_index] is None:
                self.hash_set[initial_index] = Bucket() #make a bucket at an index which contains nothing

            if key not in self.hash_set[initial_index].b_list:
                self.hash_set[initial_index].b_list.append(key) # append the key in the list the index associated will be same as that of the bucket
                self._n += 1

        elif self.collision_type == 'Linear':
            index = initial_index

            while self.hash_set[index] is not None:
                if self.hash_set[index] == key: # duplicate found 
                    return
                index = (index + 1)% self.hash_set_size # take steps of one unit
                if index == initial_index: # toatal unsuccesful probes reached
                    return
            self.hash_set[index] = key
            self._n += 1

        elif self.collision_type == 'Double':
            index = initial_index
            h2_index = self.h2(key,self.params[1],self.params[2]) # finding the jump magnitude using second hash function

            for i in range(self.hash_set_size):
                index = (initial_index + i*h2_index)% self.hash_set_size
                if self.hash_set[index] is None: # if the index is empty
                    self.hash_set[index] = key
                    self._n += 1
                    return 
                elif self.hash_set[index] == key: # if the key was already present at some index
                    return
                #update the index taking steps size h2_index
            return 
                                               
    
    def find(self, key):
            initial_index = self.get_slot(key)

            if self.collision_type == 'Chain':
                if self.hash_set[initial_index] is not None:
                    if key in self.hash_set[initial_index].b_list:
                        return True
                return False

            elif self.collision_type == 'Linear':
                index = initial_index
                for _ in range(self.hash_set_size):
                    if self.hash_set[index] == key:
                        return True
                    if self.hash_set[index] is None:
                        break
                    index = (index + 1) % self.hash_set_size
                return False     

            elif self.collision_type == 'Double':
                index = initial_index
                h2_index = self.h2(key,self.params[1],self.params[2])
                for i in range(self.hash_set_size):
                    if self.hash_set[index] == key:
                        return True
                    if self.hash_set[index] is None:
                        break
                    index = (initial_index + i * h2_index) % self.hash_set_size
                return False                

    
    def get_slot(self, key):
        initial_index = self.h1(key,self.params[0],self.hash_set_size)
        return initial_index

    
    def get_load(self):
        load = self._n/self.hash_set_size
        return load
    
    def __str__(self):
        slot_strings = []

        for slot in self.hash_set:
            if slot is None:
                slot_strings.append("<EMPTY>")

            elif isinstance(slot,Bucket):# for chaining
                bucket_contents = " ; ".join(str(key) for key in slot.b_list)
                slot_strings.append(bucket_contents)

            else: # for linear or double probing
                slot_strings.append(str(slot))

        #join all with separator " | "
        return " | ".join(slot_strings)

        
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
        self.hash_map_size = self.params[-1]
        self.hash_map = self.hash_map_size*[None]
        self._n = 0 #no of elements
    
    def insert(self, x):
        # x = (key, value)
        initial_index = self.h1(x[0], self.params[0],self.hash_map_size)

        if self.collision_type == 'Chain':
            if self.hash_map[initial_index] is None:
                self.hash_map[initial_index] = Bucket() #make a bucket at an index which contains nothing

            if x not in self.hash_map[initial_index].b_list:
                self.hash_map[initial_index].b_list.append(x) # append the key in the list the index associated will be same as that of the bucket
                self._n += 1

        elif self.collision_type == 'Linear':
            index = initial_index

            while self.hash_map[index] is not None:
                if self.hash_map[index] == x: # duplicate found 
                    return
                index = (index + 1)% self.hash_map_size # take steps of one unit
                if index == initial_index: # toatal unsuccesful probes reached
                    return
            self.hash_map[index] = x
            self._n += 1

        elif self.collision_type == 'Double':
            index = initial_index
            h2_index = self.h2(x[0],self.params[1],self.params[2]) # finding the jump magnitude using second hash function

            for i in range(self.hash_map_size):
                index = (initial_index + i*h2_index)% self.hash_map_size
                if self.hash_map[index] is None: # if the index is empty
                    self.hash_map[index] = x
                    self._n += 1
                    return 
                elif self.hash_map[index] == x: # if the key was already present at some index
                    print("duplicate found")
                    return
                #update the index taking steps size h2_index
                
            
    
    def find(self, key):
        initial_index = self.get_slot(key)

        if self.collision_type == 'Chain':
            if self.hash_map[initial_index] is not None:
                for entry in self.hash_map[initial_index].b_list:  
                    if entry[0] == key:  
                        return entry[1]
            return None

        elif self.collision_type == 'Linear':
            index = initial_index
            for _ in range(self.hash_map_size):
                if self.hash_map[index][0] == key:
                    return self.hash_map[index][1]
                if self.hash_map[index] is None:
                    break
                index = (index + 1) % self.hash_map_size
            return None           
    
        elif self.collision_type == 'Double':
            index = initial_index
            h2_index = self.h2(key,self.params[1],self.params[2])
            for i in range(self.hash_map_size):
                if self.hash_map[index][0] == key:
                    return self.hash_map[index][1]
                if self.hash_map[index] is None:
                    break
                index = (initial_index + i * h2_index) % self.hash_map_size
            return None
        
    def get_slot(self, key):
        initial_index = self.h1(key,self.params[0],self.hash_map_size)
        return initial_index
    
    def get_load(self):
        load = self._n/self.hash_map_size
        return load
    
    def __str__(self):
        ans = []

        for slot in self.hash_map:
            if slot is None:
                ans.append("<EMPTY>")
            elif isinstance(slot,Bucket):
                bucket_contents = " ; ".join(f"({x[0]},{x[1]})" for x in slot.b_list)
                ans.append(bucket_contents)
            else:
                ans.append(f"({slot[0]},{slot[1]})")

        return " | ".join(ans)

class Bucket:
    def __init__(self):
        self.b_list = []


   