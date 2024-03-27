#This code segment uses a breadth first search algorithm to find the shortest route through a given maze. 
#The user is allowed to create their own maze using nested lists. 
#The algorithm will recognize the ‘#’ char as obstacles and boundaries, and ‘ ’ (empty spaces) as valid paths. 
#The code uses the curses module to display the maze in the terminal. 
#For the BFS algorithm we use a queue as an underlying data structure. 
#The queue is used to process nodes and then look at the neighbors of those nodes and add them to the queue. 
#It will iteratively process the neighbors until it arrives at the shortest path to the end of the maze 
#while displaying its progress in the terminal.

import curses       #Gives us stdscr and colors and wrapper
from curses import wrapper
import queue           #Imports the queue data structure
import time     #Allows us to have a delay when drawing our path

maze = [            #Maze constructed out of nested lists
    ["#", "#", "#", "#", "O", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

    ###Prints Maze###
def print_maze(maze, stdscr, path=[]):      #inputs maze, stdscr, and path
    BLUE = curses.color_pair(1)   #Sets BLUE to the blue and black color pair from main using index 1
    RED = curses.color_pair(2)    #Sets RED to the red and black color pair from main using index 2

    for i, row in enumerate(maze):      #Iterates through every row (nested list)   
        for j, value in enumerate(row):     #Iterates through every character in row (character in nested list)
            if (i, j) in path:              #Checks if current position is in the path
                stdscr.addstr(i, j*2, "X", RED) #If true: adds a red X to the screen to indicate that it is a part of the path
            else:
                stdscr.addstr(i, j*2, value, BLUE)      #Adds each character of maze variable onto screen(j*2 spreads the cols out)

###Finds the starting point of maze###
def find_start(maze, start):            #Inputs the maze and start variable
    for i, row in enumerate(maze):      #Iterates through every row (nested list)   
        for j, value in enumerate(row): #Iterates through every character in row (character in nested list)
            if value == start:          #Checks if the value is O
                return i, j             #If true return the position
            
    return None     #Return none if start was not found
            
###Breadth First Search Algorithm###
def find_path(maze, stdscr):        #inputs maze and stdscr
    start = "O"             #Start char = O
    end = "X"               #End char = X
    start_pos = find_start(maze, start)     #calls find_start function and stores the row and col of the start position

    q = queue.Queue()           #initializes a queue data structure for the BFS algorithm, which stores tuples of a node's position and the path to reach it.
    q.put((start_pos, [start_pos])) #Adds a tuple which stores the start pos and a list containing the path

    visited = set()     #Set that will contain all positions that have already been visited (esures that the algorithm does not loop back)

    while not q.empty():            #While we have not found the end node
        current_pos, path = q.get()     #Recieves the element at the front of the queue and sets it to the current pos and the path
        row, col = current_pos      #seperates current pos into row and col(i and j)

        stdscr.clear()              #Clears the screen
        print_maze(maze, stdscr, path)  #Draws the maze with the path
        time.sleep(0.2)     #adds a 0.2 second delay between every step
        stdscr.refresh()       #adds changes to maze
        
        ###Makes sure to stop iterating once we have found the end###
        if maze[row][col] == end:       #Checks if maze at current position is the end
            return path                 #If true return the path

        neighbors = find_neighbors(maze, row, col)  #calls find_neighbors function and stores all neighbors of current node

        for neighbor in neighbors:      #Iterates through all neighbors in the neighbors list
            if neighbor in visited:     #If we have already visited neighbor
                continue                #Continue to next neighbor(do not process it)
        
            r, c = neighbor         #Sets r c to position of neighbors
            if maze[r][c] == "#":   #Checks if value of neighbor is '#' (not a valid path for exploration)
                continue            #If true continue to next neighbor (do not process)
                
            new_path = path + [neighbor]    #Adds position of neighbor to the current path
            q.put((neighbor, new_path))     #adds position of neighbor and new path into the queue
            visited.add(neighbor)           #Adds neighbor to visited(so it is not processed again)

###Finds neighbors of a node###
def find_neighbors(maze, row, col):     #Inputs the maze and position of current node
    neighbors = []                      #Stores neighbors of current node

    if row > 0: #Checks if row is not at the top of the maze (node has an upper neighbor)
        neighbors.append((row - 1, col))    #If true adds position of above neighbor of current node to neighbors list
    if row + 1 < len(maze): #Checks if row is not on the bottom of the maze(row has a lower neighbor)
        neighbors.append((row + 1, col))    #If true adds position of lower neighbor of current node to neighbors list
    if col > 0: #Checks if col is not the leftmost column(node has a left neighbor)
        neighbors.append((row, col - 1))    #If true adds position of left neighbor of current node to neighbors list
    if col + 1 < len(maze[0]): #Checks if col is not the rightmost column(node has a right neighbor)
        neighbors.append((row, col + 1))    #If true adds position of right neighbor of current node to neighbots list

    return neighbors #Returns neighbors of current node


def main(stdscr): #stdscr takes over terminal as a window object and represents a screen in a curses application
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #(id, foreground color, background color)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr) #Navigates shortest route through maze and takes the maze and stdscr as parameters
    stdscr.getch()   #Exits the std screen when a key is pressed       


wrapper(main)   #initializes curses module and calls main and passes stdscr