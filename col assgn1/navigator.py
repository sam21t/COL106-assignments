from maze import *
from exception import *
from stack import *

class PacMan:
    def __init__(self, grid : Maze) -> None:
        ## DO NOT MODIFY THIS FUNCTION
        self.navigator_maze = grid.grid_representation
        self.grid = grid
        
    def valid_move(self,x,y,navigator_maze,visited):
        rows, cols = len(navigator_maze), len(navigator_maze[0])
        return 0 <= x < rows and 0<= y < cols and navigator_maze[x][y] == 0 and not visited[x][y]       
        
    def find_path(self, start, end):
        # IMPLEMENT FUNCTION HERE
       if self.grid.is_ghost(start[0],start[1]):
           raise PathNotFoundException
       
       rows, cols = len(self.navigator_maze), len(self.navigator_maze[0])
       
       stack = Stack()
       stack.push(start,[start])
       
       visited = [[False for a in range(cols)]for a in range(rows)]
       visited[start[0]][start[1]]=True
       
       steps=[(0,1),(1,0),(-1,0),(0,-1)]
       
       while not stack.is_empty():
           (current,path)=stack.pop()
           x,y= current
           
           if(x,y)==end:
               return path
               
           for dx, dy in steps:
               nx, ny = x+dx,y+dy
               if self.valid_move(nx,ny,self.navigator_maze,visited):
                   stack.push((nx,ny), path + [(nx,ny)])
                   visited[nx][ny]=True
        
          
       raise PathNotFoundException