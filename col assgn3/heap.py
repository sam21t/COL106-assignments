
'''
Python Code to implement a heap with general comparison function
'''
# to generate min heap
def comp_min_crew(arg1,arg2):
    if arg2.load > arg1.load:
        return True
    return False

def comp_min_tr(arg1,arg2):
    if (arg1.arrival_time + arg1.rem_size()) != (arg2.arrival_time + arg2.rem_size()):
        if (arg2.arrival_time +arg2.rem_size()) > (arg1.arrival_time + arg1.rem_size()):
            return True
        else:
            return False
    else:
        if arg2.id>arg1.id:
            return True
        return False    



class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        
        # Write your code here
        self.comp_function = comparison_function
        self.heap = init_array.copy()
        self.size = len(init_array)
        self.build_heap()
        
    def insert(self, value): #value is an tuple
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
         #increment size and insert at the end of array then call upheap on that element
        self.heap.append(value)
        self.size +=1
        self.upheap(self.size -1)
        
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        if self.size ==0:
            return None
        if self.size == 1:
            self.size -= 1
            return self.heap.pop()
            
        
        topmost = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.size -=1
        self.downheap(0)
        return topmost
        
    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        # Write your code here
        if self.size ==0:
            return None
        return self.heap[0]
    
    # You can add more functions if you want to
    def parent(self,pos):
        return (pos-1)//2
    
    def leftchild(self,pos):
        return 2*pos + 1
    
    def rightchild(self,pos):
        return (2*pos) + 2
    
    def isLeaf(self,pos):
        return pos >= self.size//2 and pos < self.size
    
    def swap(self, pos1, pos2):
        self.heap[pos1] , self.heap[pos2] = self.heap[pos2], self.heap[pos1]

    #upheap operation
    def upheap(self,pos):
        if pos > 0 and self.comp_function(self.heap[pos],self.heap[self.parent(pos)]):
            self.swap(pos,self.parent(pos))
            self.upheap(self.parent(pos))
        else:
            return None

    #downheap operation
    def downheap(self,pos):
        if not self.isLeaf(pos):
            left = self.leftchild(pos)
            right = self.rightchild(pos)
            selected = pos

            if left < self.size and self.comp_function(self.heap[left], self.heap[selected]):
                selected =left
            if right < self.size and self.comp_function(self.heap[right], self.heap[selected]):
                selected = right
            #recursive downheap
            if selected != pos:
                self.swap(pos, selected)
                self.downheap(selected)
        else:
            return None


    #building the heap
    def build_heap(self):
        # till -1 as we are starting with index 0 in the array
        for pos in range(self.size//2 -1, -1, -1):
            self.downheap(pos)


    def print_heap(self):
        for i in range(self.size):
            left = self.leftchild(i)
            right = self.rightchild(i)
            
            print(f"PARENT: {self.heap[i].id,self.heap[i].rem_size()+self.heap[i].arrival_time}", end=" ")
            
            if left < self.size:
                print(f"LEFT CHILD: {self.heap[left].id,self.heap[left].rem_size()+self.heap[left].arrival_time}", end=" ")
            
            if right < self.size:
                print(f"RIGHT CHILD: {self.heap[right].id,self.heap[i].arrival_time+self.heap[i].rem_size()}", end="")
            
            print()  # New line for next parent