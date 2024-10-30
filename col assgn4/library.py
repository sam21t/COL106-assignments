import hash_table as ht
from hash_table import Bucket

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        self.book_titles = book_titles
        self.texts = texts
        self.book_words = []

        for i in range(len(self.book_titles)):
            texts_copy = self.texts[i].copy()
            distinct_words = self.get_distinct_words(texts_copy)
            self.book_words.append((self.book_titles[i],distinct_words))
        
        self.merge_sort(self.book_words)

        for i in range(len(self.book_words)):
            title , words_list = self.book_words[i]
            self.merge_sort(words_list)
            self.book_words[i] = (title, words_list)
      
    
    def distinct_words(self, book_title):
        #binary search for the book then access its words
        selected_book_index = self.bin_search(self.book_words,book_title)
        if selected_book_index == -1:
            return []
        selected_book_words = self.book_words[selected_book_index][1]
        return selected_book_words
    
    def count_distinct_words(self, book_title):
        #binary search for the book then tell the length of its list of words
        selected_book_index = self.bin_search(self.book_words,book_title)
        return len(self.book_words[selected_book_index][1])
    
    def search_keyword(self, keyword):
        #create empty list to store favourable books having the word
        selected_books = []

        for i in self.book_words:
            check = False
            if(self.bin_search_words(i[1],keyword)>=0):
                #if binary search returns positive then word exists in that book
                check = True
            if check:
                selected_books.append(i[0])
            
        return selected_books
    
    def print_books(self):
        for book_title, words_list in self.book_words:
            formatted_words = " | ".join(words_list)
            print(f"{book_title}: {formatted_words}")


    def merge(self,left,right,word_list):
        i=j=0

        #compare elements from both halves
        while i+j < len(word_list):
            if j==len(right) or (i<len(left) and left[i]<right[j]):
                word_list[i+j] = left[i]
                i +=1
            else:
                word_list[i+j]= right[j]
                j += 1

    def merge_sort(self,word_list):
        #base case
        if len(word_list) <= 1:
            return 
        
        #divide
        mid = len(word_list)//2
        left_half = word_list[0:mid]
        right_half = word_list[mid:len(word_list)]

        #recursive call
        self.merge_sort(left_half)
        self.merge_sort(right_half)

        #merge
        self.merge(left_half,right_half,word_list)

    def get_distinct_words(self,words_list):
        #sort the list of words first then we can remove duplicates in one scan
        self.merge_sort(words_list)

        #remove duplicates now
        distinct = []
        if len(words_list) > 0:
            distinct.append(words_list[0]) 
            for i in range(1, len(words_list)):
                if words_list[i] != words_list[i - 1]:  
                    distinct.append(words_list[i])
        return distinct
    
    def bin_search(self,d_word_list,target):
        low = 0
        high = len(d_word_list)-1

        while(low<=high):
            mid = low + (high-low)//2
            if d_word_list[mid][0]==target:
                return mid
            elif d_word_list[mid][0]<target:
                low = mid +1
            else:
                high = mid-1

        return -1 
    
    def bin_search_words(self,word_list,target):
        low = 0
        high = len(word_list)-1

        while(low<=high):
            mid = low + (high-low)//2
            if word_list[mid]==target:
                return mid
            elif word_list[mid]<target:
                low = mid +1
            else:
                high = mid-1

        return -1 
           

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name = name
        self.params = params

        if self.name == 'Jobs':
            self.lib_hash_map = ht.HashMap("Chain",self.params)
        elif self.name == 'Gates':
            self.lib_hash_map = ht.HashMap("Linear",self.params)
        elif self.name == 'Bezos':
            self.lib_hash_map = ht.HashMap("Double", self.params)

    
    def add_book(self, book_title, text):
        if self.name == 'Jobs':
            words_hashset = ht.HashSet("Chain",self.params)
            for word in text:
                words_hashset.insert(word)

            self.lib_hash_map.insert((book_title,words_hashset))

        elif self.name == 'Gates':
            words_hashset = ht.HashSet("Linear",self.params)
            for word in text:
                words_hashset.insert(word)
            
            self.lib_hash_map.insert((book_title,words_hashset))

        elif self.name == 'Bezos':
            words_hashset = ht.HashSet("Double",self.params)
            for word in text:
                words_hashset.insert(word)
            
            self.lib_hash_map.insert((book_title,words_hashset))           

    def distinct_words(self, book_title):
        words_hashset = self.lib_hash_map.find(book_title)

        if words_hashset is None:
            return []
        
        distinct_words = []
        for slot in words_hashset.hash_set:
            if slot is not None:
                if isinstance(slot,Bucket):
                    distinct_words.extend(slot.b_list)
                else:
                    distinct_words.append(slot)

        return distinct_words
    
    def count_distinct_words(self, book_title):
        words_hashset = self.lib_hash_map.find(book_title)
        if words_hashset is None:
            return 0
        return words_hashset._n  
    
    def search_keyword(self, keyword):
        selected_books = []

        for slot in self.lib_hash_map.hash_map:
            if slot is not None:
                if isinstance(slot,Bucket): # case of chaining
                    for entry in slot.b_list:
                        book_title, words_hashset = entry
                        # check if keyword present
                        if words_hashset.find(keyword):
                            selected_books.append(book_title)
                    
                else:# for the case of linear and double
                    book_title, words_hashset = slot
                    if words_hashset.find(keyword):
                        selected_books.append(book_title)

        return selected_books
    
    def print_books(self):
        for slot in self.lib_hash_map.hash_map:
            if slot is not None:
                if isinstance(slot,Bucket):
                    for book_title, words_hashset in slot.b_list:
                        print(f"{book_title}: {str(words_hashset)}")
                else:
                    book_title, words_hashset = slot
                    print(f"{book_title}: {str(words_hashset)}")