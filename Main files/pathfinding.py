import pygame, Rooms, heapq

def heuristic(a, b): #creates a heuristic function for A* algorithm
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) #Manhattan distance between two points

def get_neighbours (node, room): #gets neighboring walkable tiles
    x, y = node 
    neighbours = [] #create list to store neighboring floor tiles
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] #up, right, down, left
    
    #directional movement
    for direction_x, direction_y in directions: #for each direction
        neighbour_x, neighbour_y = x + direction_x, y + direction_y #calculate neighbor position
        
        if 0 <= neighbour_x < room.width and 0 <= neighbour_y < room.height: #check bounds of room (walls)
            if room.template[neighbour_y][neighbour_x] == 1: #check if tile is walkable (floor)
                neighbours.append((neighbour_x, neighbour_y)) #add to neighbours list
                
    return neighbours

def astar(room, start, goal): #A* pathfinding algorithm
    open_set = [] #list of nodes/tiles to explore
    heapq.heappush(open_set, (0, start)) #add node with lowest f_score/heuristic value to start with
    
    came_from = {} #dictionary to track best path/previous nodes
    g_score = {start: 0} #cost from start to current node (starts at 0)
    f_score = {start: heuristic(start, goal)} #estimated cost from start to goal through current node
    
    while open_set: #while there are nodes to explore
        current = heapq.heappop(open_set)[1] #pops node with lowest f_score
        
        if current == goal: #if goal is reached
            #reconstruct path
           
            path = [] #list to store path
            while current in came_from: #while there is a previous node
                path.append(current) #add current node to path
                current = came_from[current] #move to previous node
            path.reverse() #reverse path to get correct order from start to goal
            return path
           
        for neighbour in get_neighbours(current, room): #for each neighbor of current node
            tentative_g = g_score[current] + 1 #cost to move to neighbor (assumed to be 1)
            
            if neighbour not in g_score or tentative_g < g_score[neighbour]: #if theres a new best path to neighbor
                came_from[neighbour] = current #record where we came from
                g_score[neighbour] = tentative_g #update g_score
                f_score[neighbour] = tentative_g + heuristic(neighbour, goal) #update f_score
                heapq.heappush(open_set, (f_score[neighbour], neighbour)) #add neighbor to open set of nodes to explore
                
    return [] #return empty path if no path found