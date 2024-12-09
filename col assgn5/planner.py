from flight import Flight

def comparator(val1,val2):
    if val2[0]> val1[0]:
        return True
    elif val2[0] == val1[0] and not isinstance(val2[1],City):
        if val2[1]>val1[1]:
            return True
    return False



class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = flights
        self.G = Graph(self.flights)
    

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
            """
            Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
            arrives before t2 (<=) satisfying: 
            The route has the least number of flights, and within routes with same number of flights, 
            arrives the earliest
            """
            #making predecesor of a path that flight which will take the minimum tinme
            if start_city==end_city:
                return []
            # self.G.reset_dist()
            # self.G.reset_city_time()
            # self.G.reset_nov()
            for flight in self.flights:
                flight.dist=float('inf')

            predec = [None]*(len(self.flights))
            q = Queue()

            q.insert((0,None,self.G.nodes[start_city]))
            best=[float('inf'),float('inf'),None]
        

            while q.empty() == False:
                
                top_node = q.peek()
                q.remove()
                if top_node[1] is not None:
                    if (best[0],best[1])<(top_node[0],top_node[1].arrival_time):
                        continue

                if top_node[2].city_no == end_city:
                    if (best[0],best[1])>(top_node[0],top_node[1].arrival_time):
                        best=[top_node[0],top_node[1].arrival_time,top_node[1]]
                    continue

                
                if len(top_node[2].adj_list)!=0:
                    for item in top_node[2].adj_list:
                        if item is not None:
                            if top_node[1] is not None:
                                distance = top_node[0] + 1
                                if item[1].departure_time - top_node[1].arrival_time >= 20 and top_node[1].departure_time>=t1 and item[1].arrival_time<=t2:
                                    
                                    if distance < item[1].dist:
                                        predec[item[1].flight_no] = top_node[1]
                                        item[1].dist = distance
                                        q.insert((distance,item[1],self.G.nodes[item[0]]))
                            else:
                                distance = top_node[0] + 1
                                if item[1].departure_time >= t1 and item[1].arrival_time <=t2:
                                    
                                    if item[1].dist > distance:
                                        predec[item[1].flight_no] = top_node[1]
                                        item[1].dist = distance
                                        q.insert((distance,item[1],self.G.nodes[item[0]]))
                    

            #back tracking process
            ans =[]
            walk = best[2]
            while walk is not None:
                ans.append(walk)
                walk = predec[walk.flight_no]
            ans.reverse()

            if len(ans) == 0:
                return []
            elif ans[0].start_city != start_city or ans[len(ans)-1].end_city != end_city:
                return []
            return ans

    

    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        if start_city==end_city:
                return []
        # insert all paths from a city in the heap according to distance if a path fails then the next smallest path will be taken
        # self.G.reset_dist()
        # self.G.reset_city_time()
        # self.G.reset_nov()
        for flight in self.flights:
            flight.dist=float('inf')

        predec = [None]*(len(self.flights))
        min_heap = Heap(comparator,[])

        min_heap.insert((0,self.G.nodes[start_city],None))
        best=[float('inf'),None]       

        while min_heap.size > 0:
            
            top_node = min_heap.extract()

            if best[0]<top_node[0]:
                continue

            if top_node[1].city_no == end_city:
                if best[0]>top_node[0]:
                    best=[top_node[0],top_node[2]]

            
            if len(top_node[1].adj_list)!=0:
                for item in top_node[1].adj_list:
                    if item is not None:
                        if top_node[2] is not None:
                            distance = top_node[0] + item[1].fare
                            if item[1].departure_time - top_node[2].arrival_time >= 20 and top_node[2].departure_time>=t1 and item[1].arrival_time<=t2:
                                
                                if distance < item[1].dist:
                                    predec[item[1].flight_no] = top_node[2]
                                    item[1].dist = distance
                                    min_heap.insert((distance,self.G.nodes[item[0]],item[1]))
                        else:
                            distance = top_node[0] + item[1].fare
                            if item[1].departure_time >= t1 and item[1].arrival_time <=t2:
                                
                                if item[1].dist > distance:
                                    predec[item[1].flight_no] = top_node[2]
                                    item[1].dist = distance
                                    min_heap.insert((distance,self.G.nodes[item[0]],item[1]))
                

        #back tracking process
        ans =[]
        walk = best[1]
        while walk is not None:
            ans.append(walk)
            walk = predec[walk.flight_no]
        ans.reverse()

        if len(ans) == 0:
            return []
        elif ans[0].start_city != start_city or ans[len(ans)-1].end_city != end_city:
            return []
        return ans

    
    

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        if start_city==end_city:
                return []
        # same process as part 2 but here number of visits to a city take preference over the distance 
        # self.G.reset_dist()
        # self.G.reset_city_time()
        # self.G.reset_nov()
        for flight in self.flights:
            flight.dist=float('inf')
            flight.ffare=float('inf')

        predec = [None]*(len(self.flights))
        min_heap = Heap(comparator,[])

        min_heap.insert((0,0,self.G.nodes[start_city],None))
        best=[float('inf'),float('inf'),None]
       

        while min_heap.size > 0:
            
            top_node = min_heap.extract()
            
            if (best[0],best[1])<(top_node[0],top_node[1]):
                continue

            if top_node[2].city_no == end_city:
                if (best[0],best[1])>(top_node[0],top_node[1]):
                    best=[top_node[0],top_node[1],top_node[3]]
                continue
            
            if len(top_node[2].adj_list)!=0:
                for item in top_node[2].adj_list:
                    if item is not None:
                        if top_node[3] is not None:
                            numb = top_node[0] + 1
                            if item[1].departure_time - top_node[3].arrival_time >= 20 and top_node[3].departure_time>=t1 and item[1].arrival_time<=t2:
                                distance = top_node[1] + item[1].fare

 
                                if (item[1].dist,item[1].ffare)>(numb,distance):
                                    item[1].dist=numb
                                    item[1].ffare=distance
                                    predec[item[1].flight_no] = top_node[3]                         


                                    min_heap.insert((numb,distance,self.G.nodes[item[0]],item[1]))
                        else:
                            numb = top_node[0] + 1
                            if item[1].departure_time >= t1 and item[1].arrival_time<=t2:
                                distance = top_node[1] + item[1].fare

                                if (item[1].dist,item[1].ffare)>(numb,distance):
                                    item[1].dist=numb
                                    item[1].ffare=distance
                                    predec[item[1].flight_no] = top_node[3]


                                    min_heap.insert((numb,distance,self.G.nodes[item[0]],item[1]))

               
        # back tracking process
        ans =[]
        walk = best[2]
        while walk is not None:
            ans.append(walk)
            walk = predec[walk.flight_no]
        ans.reverse()

        if len(ans) == 0:
            return []
        elif ans[0].start_city != start_city or ans[len(ans)-1].end_city != end_city:
            return []
        return ans


class Graph:
    def __init__(self,flights):
        self.nodes = []
        temp=self.get_max_city_no(flights)
        for i in range(temp+1):
            self.nodes.append(City(i))

        for flight in flights:
            self.nodes[flight.start_city].adj_list.append((flight.end_city,flight))

    def add_city(self,city_obj):
        self.nodes.append(city_obj)

    def add_edge(self,start,end,flight_obj):
        if start and end:
            start.adj_list.append((end.city_no,flight_obj))

    def get_max_city_no(self,flights_list):
        max_val = 0
        for flight in flights_list:
            if max(flight.start_city,flight.end_city)>= max_val:
                max_val = max(flight.start_city,flight.end_city)
        
        return max_val
    
    def reset_city_time(self):
        for city in self.nodes:
            city.time = float('inf')

    def reset_dist(self):
        for city in self.nodes:
            city.dist = float('inf')

    def reset_nov(self):
        for city in self.nodes:
            city.nov = float('inf')


class City:
    def __init__(self,city_no):
        self.city_no = city_no
        self.adj_list = []
        self.time = float('inf')
        self.dist = float('inf')
        self.nov = float('inf')


class Queue:
    def __init__(self):
        self.array=[]
        self.curr_size=0
        self.l=0

    def insert(self,val):
        self.array.append(val)
        self.curr_size+=1
        return
    
    def remove(self):
        self.l+=1
        return
    
    def peek(self):
        return self.array[self.l]

    def empty(self):
        return self.l>=self.curr_size


class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array):
        
        # Write your code here
        self.comp_function = comparison_function
        self.heap = init_array.copy()
        self.size = len(init_array)
        self.build_heap()
        
    def insert(self, value): #value is a tuple
        
        # Write your code here
         #increment size and insert at the end of array then call upheap on that element
        self.heap.append(value)
        self.size +=1
        self.upheap(self.size -1)
        
    
    def extract(self):
        
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

