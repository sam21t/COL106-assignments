from bin import Bin
from avl import AVLTree, comp_bg, comp_ry, comp_obj
from node import Node
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        self.bins_bg = AVLTree(compare_function=comp_bg)
        self.bins_ry = AVLTree(compare_function=comp_ry)
        self.all_bins = AVLTree(compare_function=comp_obj)
        self.obj_tree = AVLTree(compare_function=comp_obj)

    def add_bin(self, bin_id, capacity):
        new_bin= Bin(bin_id,capacity)
        self.bins_bg.insert_node(new_bin)
        self.bins_ry.insert_node(new_bin)
        self.all_bins.insert_node(new_bin)
            
    def add_object(self, object_id, size, color):
      if color == Color.GREEN:
        selected_node = self.add_green(size)
      elif color == Color.BLUE:
        selected_node = self.add_blue(size)
      elif color == Color.RED:
        selected_node = self.add_red(size)
      else:  # YELLOW
        selected_node = self.add_yellow(size)
    
      if selected_node is None:
        raise NoBinFoundException
    
      req=self.all_bins.normalsearch(self.all_bins.root,selected_node.value)
      req.value.add_object(object_id,size,color)
      temp = selected_node.value
      self.update_bin_capacity(temp.id,(temp.capacity-size))


      newobj=Object(object_id,size,color,temp.id)
      
      self.obj_tree.insert_node(newobj)
      
      return

    def object_info(self, object_id):

        selected_obj = self.obj_tree.get_by_id(object_id)

        if selected_obj is None:
            return None

        bin_ki_id = selected_obj.value.storage

        return bin_ki_id

    def delete_object(self, object_id):
        # # Implement logic to remove an object from its bin

        selected_obj_node = self.obj_tree.get_by_id(object_id)
        obj_to_be_removed = selected_obj_node.value
        temp = obj_to_be_removed.capacity
        
        binid = obj_to_be_removed.storage
        
        bin_node = self.all_bins.get_by_id(binid)
        temp_bin = bin_node.value
        
        if bin_node:
            self.bins_bg.delete_node(bin_node)
            self.bins_ry.delete_node(bin_node)
            
            bin_node.value.remove_object(object_id)
            self.obj_tree.delete_node(selected_obj_node)
            
            temp_bin.capacity += temp 
            
            self.bins_ry.insert_node(temp_bin)
            self.bins_bg.insert_node(temp_bin)
            

        return
        
    def bin_info(self, bin_id):
      bin_node = self.all_bins.get_by_id(bin_id)
      if bin_node is None:
        return None  # bin not found
    
      bin_value = bin_node.value
      ans=[]
      bin_value.avl_tree.traverse(bin_value.avl_tree.root,ans)
      finalans=[]
      finalans.append(bin_value.capacity)
      finalans.append(ans)

      return tuple(finalans)



    def update_bin_capacity(self, bin_id, new_capacity):
    # Find the bin in the all_bins tree
        bin_node = self.all_bins.get_by_id(bin_id)
        if bin_node is None:
            raise Exception(f"Bin with ID {bin_id} not found.")  # Raise an error if not found
        req_cap = bin_node.value.capacity
        
        # Create a temporary Bin for searching
        bin_node_bg = self.bins_bg.normalsearch(self.bins_bg.root, bin_node.value)
        bin_node_ry = self.bins_ry.normalsearch(self.bins_ry.root, bin_node.value)

        temp=bin_node.value.avl_tree
        # Delete the old nodes from all trees
        self.all_bins.delete_node(bin_node)
        self.bins_bg.delete_node(bin_node_bg)
        self.bins_ry.delete_node(bin_node_ry)

        # Create a new bin object with updated capacity
        new_bin = Bin(bin_id, new_capacity)
        new_bin.avl_tree = temp  # Preserve the objects in the bin

        # Insert the new node into all trees
        self.all_bins.insert_node(new_bin)
        self.bins_bg.insert_node(new_bin)
        self.bins_ry.insert_node(new_bin)

        return

        
    
    def add_green(self, size):
        candidate=self.bins_bg.root
        while candidate.right:
            candidate=candidate.right
        if candidate.value.capacity<size:
            return None
        else:
            return candidate

    def add_red(self, size):
        candidate=self.bins_ry.root
        while candidate.right:
            candidate=candidate.right
        if candidate.value.capacity<size:
            return None
        else:
            return candidate
      

    def add_blue(self, size):
        candidate=self.bins_bg.root
        best=None
        while candidate:
            if candidate.value.capacity<size:
                candidate=candidate.right
            else:
                best=candidate
                candidate=candidate.left
        return best
        
    def add_yellow(self, size):
        candidate=self.bins_ry.root
        best=None
        while candidate is not None:
            if candidate.value.capacity<size:
                candidate=candidate.right
            else:
                best=candidate
                candidate=candidate.left
        return best