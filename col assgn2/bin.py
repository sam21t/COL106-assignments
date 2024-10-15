from object import Object
from avl import AVLTree

class Bin():
    def __init__(self, bin_id, capacity):
        self.id = bin_id
        self.capacity = capacity
        self.avl_tree = AVLTree()

    def add_object(self, obj_id,size,color):
        # Implement logic to add an object to this bin
        object_1=Object(obj_id,size,color)
        self.avl_tree.insert_node(object_1)

    
    def remove_object(self, obj_id):
        # Implement logic to remove an object by ID
        self.avl_tree.root = self.avl_tree.delete_by_id(self.avl_tree.root,obj_id)
