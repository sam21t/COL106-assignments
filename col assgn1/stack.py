
class Stack:
    def __init__(self) -> None:
        #YOU CAN (AND SHOULD!) MODIFY THIS FUNCTION
         self.stack = []
    # You can implement this class however you like
    def push(self, item, path):
        self.stack.append((item,path))
        
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.stack.pop()
        
    def is_empty(self):
        return len(self.stack) == 0 