from node import Node

def comp_bg(node_1, node_2):
        #capacity comparision
        if node_1.capacity != node_2.capacity:
            return node_1.capacity - node_2.capacity
        else:
            #id comparision
            return node_1.id - node_2.id

def comp_ry(node_1,node_2): #nodes are either objects or bins
            if node_1.capacity != node_2.capacity:
               return node_1.capacity - node_2.capacity
            else:
            #id comparision
               return node_2.id - node_1.id
    
        
def comp_obj(node_1, node_2):
    return node_1.id - node_2.id

class AVLTree:
    def __init__(self, compare_function=comp_obj):
        self.root = None
        self.size = 0
        self.comparator = compare_function
        
    #getting height of element
    def _get_height(self, element):
        if not element:
            return 0;
        return element.height
        
    #checking balance of the element
    def _get_balance(self, element):
        if not element:
            return 0;
        return self._get_height(element.left) - self._get_height(element.right)
        
    #right rotation implementation
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        #rotate
        x.right = y
        y.left = T2
        # height reset
        x.height = max(self._get_height(x.left),self._get_height(x.right))+1
        y.height = max(self._get_height(y.left),self._get_height(y.right))+1
        return x
        
    #left rotation implementation
    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        #rotate
        y.left = x
        x.right = T2
        #height reset
        x.height = max(self._get_height(x.left),self._get_height(x.right))+1
        y.height = max(self._get_height(y.left),self._get_height(y.right))+1
        return y
        
    # insertion function
    def insert(self, root, element):
        #BST insertion
        if not root:
            return Node(element)
        
        # using comparator for insertion 
        if self.comparator(element, root.value)< 0:
            root.left = self.insert(root.left, element)
        else:
            root.right = self.insert(root.right, element)
            
        #update the height of ancestor
        root.height = 1 + max(self._get_height(root.left),self._get_height(root.right))
        
        #find the balance factor 
        balance = self._get_balance(root)
        
        #checking for imbalance and doing the rotations
        #LL
        if balance > 1 and self.comparator(element, root.left.value)<0:
            return self._right_rotate(root)
            
        ##RR
        if balance <-1 and self.comparator(element, root.right.value)>0:
            return self._left_rotate(root)
            
        ##LR
        if balance >1 and self.comparator(element, root.left.value)>0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        
        #RL
        if balance <-1 and self.comparator(element, root.right.value)<0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
            
        return root
        
    #inserting a new element in the tree
    def insert_node(self, element):
        self.root = self.insert(self.root, element)
        self.size += 1
        
    #deleting function
    def delete(self, root, key_node):
        if root is None:
            return root
            
        if self.comparator(key_node.value,root.value)>0:
            root.right = self.delete(root.right, key_node)
        elif self.comparator(key_node.value,root.value)<0:
            root.left = self.delete(root.left, key_node)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            #element with both left and right child(finding inorder successor)
            temp = self._get_min_value_node(root.right)
            root.value=temp.value
            root.right = self.delete(root.right, temp)

        if root is None:
            return root
            
        #update height
        root.height = 1 + max(self._get_height(root.left),self._get_height(root.right))
        
        #balance the element 
        balance = self._get_balance(root)
        
        #checking for imbalance and doing the rotations
        #LL
        if balance > 1 and self._get_balance(root.left)>=0:
            return self._right_rotate(root)
            
        ##RR
        if balance <-1 and self._get_balance(root.right)<=0:
            return self._left_rotate(root)
            
        ##LR
        if balance >1 and self._get_balance(root.left)<0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        
        #RL
        if balance <-1 and self._get_balance(root.right)>0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
            
        return root
        
    #deleting a element 
    def delete_node(self, element):
        self.root = self.delete(self.root, element)
        self.size -= 1
        
    #finding min value element after a element (successor)
    def _get_min_value_node(self, element):
        current = element
        while current.left:
            current = current.left
        return current       
        
    #finding a element by ID (basically a utility function)    
    def get_by_id(self, bin_id):
        result = self._find_by_id(self.root, bin_id)
        # print(f"Searching for bin_id {bin_id}, result: {'Found' if result else 'Not Found'}")
        return result
        
    def _find_by_id(self, element, bin_id):
        if element is None:
            return None
            
        elif element.value.id == bin_id:
            return element
        elif bin_id < element.value.id and element.left is not None:
            return self._find_by_id(element.left,bin_id)
        elif bin_id > element.value.id and element.right is not None:
            return self._find_by_id(element.right,bin_id)
        


    def traverse(self,root,finallist):
        if not root:
            return
        self.traverse(root.left,finallist)
        finallist.append(root.value.id)
        self.traverse(root.right,finallist)

    

            
    def delete_by_id(self, root, key):
      if root is None:
         return root

      # If the key to be deleted is smaller 
      # than the root's key, then it lies in 
      # left subtree
      if key < root.value.id:
          root.left = self.delete_by_id(root.left, key)

      # If the key to be deleted is greater 
      # than the root's key, then it lies in 
      # right subtree
      elif key > root.value.id:
          root.right = self.delete_by_id(root.right, key)

      # if key is same as root's key, then 
      # this is the node to be deleted
      else:
          # node with only one child or no child
          if root.left is None or root.right is None:
              temp = root.left if root.left else root.right

              # No child case
              if temp is None:
                root = None
              else:  # One child case
                root = temp

          else:
            # node with two children: Get the 
            # inorder successor (smallest in 
            # the right subtree)
            temp = self._get_min_value_node(root.right)

            # Copy the inorder successor's 
            # data to this node
            root.value = temp.value

            # Delete the inorder successor
            root.right = self.delete_by_id(root.right, temp.value.id)

      # If the tree had only one node then return
      if root is None:
          return root

      root.height = max(self._get_height(root.left), 
                      self._get_height(root.right)) + 1


      balance = self._get_balance(root)

      # there are 4 cases

      # Left Left Case
      if balance > 1 and self._get_balance(root.left) >= 0:
          return self._right_rotate(root)

      # Left Right Case
      if balance > 1 and self._get_balance(root.left) < 0:
          root.left = self._left_rotate(root.left)
          return self._right_rotate(root)

      # Right Right Case
      if balance < -1 and self._get_balance(root.right) <= 0:
          return self._left_rotate(root)

      # Right Left Case
      if balance < -1 and self._get_balance(root.right) > 0:
          root.right = self._right_rotate(root.right)
          return self._left_rotate(root)

      return root

    def normalsearch(self,root,element): #element is a bin
        if not root:
            return None
        elif self.comparator(element,root.value)>0:
            return self.normalsearch(root.right,element)
        elif self.comparator(element,root.value)<0:
            return self.normalsearch(root.left,element)
        else:
            return root



