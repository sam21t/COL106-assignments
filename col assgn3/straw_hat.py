


'''
    This file contains the class definition for the StrawHat class.
'''

from crewmate import CrewMate
from heap import Heap, comp_min_crew, comp_min_tr
from treasure import Treasure

class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''
    
    def __init__(self, m):
        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''
        
        # Write your code here
        self.m = m

        self.active_crewmates = []
        self.completed =[]
        self.all_treasures = []

        #list having all crewmate objects
        crewmates = [CrewMate() for i in range(m)]
        #heap creation for crewmates 
        self.crewmate_heap = Heap(comp_min_crew, crewmates)


    def add_treasure(self, treasure):
        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        
        # Write your code here

        #selecting the crewmate with least load
        x = self.crewmate_heap.extract()
        #updating it's load
        if treasure.arrival_time> x.load:
            x.load = treasure.arrival_time
        x.load += treasure.size    

        # adding the treasure in the treasure list
        x.treasure.append(treasure)
        self.all_treasures.append(treasure)
        #updating crewmate heap with that crewmate with its new load
        self.crewmate_heap.insert(x)
        #the crewmate will be active if it will work on atleat one treasure
        if len(x.treasure) == 1:
            self.active_crewmates.append(x)
    
    
    def get_completion_time(self):
        '''
        Arguments:
            None
        Returns:
            List[Treasure] : List of treasures in the order of their completion after updating Treasure.completion_time
        Description:
            Returns all the treasure after processing them
        Time Complexity:
            O(n(log(m) + log(n))) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        
        # Reset treasure state before starting
        self.reset_treasure_state()

        for x in self.active_crewmates:
            new = Heap(comp_min_tr, [])  # min-heap for treasures
            t = 0  # Keeps track of current time for the crewmate

            # Process each treasure of the current crewmate
            for i in range(len(x.treasure)):
                if new.size == 0:
                    # Insert first treasure and set initial time
                    new.insert(x.treasure[i])
                    t = x.treasure[i].arrival_time
                else:
                    curr = x.treasure[i].arrival_time - t  # Time difference
                    # Process treasures from heap until the time difference is accounted for
                    while new.size > 0 and curr > 0:
                        selected = new.top()  # Get the smallest treasure
                        if selected.rem_size() > curr:
                            # Process part of the treasure and update remaining capacity
                            selected.set_capacity(selected.rem_size() - curr)
                            curr = 0
                        else:
                            # Finish the treasure and update time
                            curr -= selected.rem_size()
                            selected.completion_time = t + selected.rem_size()
                            t += selected.rem_size()
                            self.completed.append(selected)
                            new.extract()  # Remove processed treasure from heap
                    
                    # Insert the next treasure and update time
                    t = x.treasure[i].arrival_time
                    new.insert(x.treasure[i])

            # Process any remaining treasures in the heap
            while new.size > 0:
                y = new.extract()
                y.completion_time = t + y.rem_size()
                t += y.rem_size()
                self.completed.append(y)

        # Sort completed treasures by their ID 
        ans = sorted(self.completed, key=lambda x: x.id)

        # Reset completed treasures for next call
        self.completed = []
        
        return ans

                

    # You can add more methods if required
    def reset_treasure_state(self):
        for tr in self.all_treasures:
            tr.reset_state()



                          
