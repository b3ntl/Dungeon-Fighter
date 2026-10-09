import pygame, random
#MAP GENERATION

pygame.init()
    
map_width = 60
map_height = 40

#create 2D array (list of lists) to represent the map
#0 = wall, 1 = floor
dungeon = [[0 for _ in range(map_width)] for _ in range(map_height)]

wall = 0
floor = 1
door = 2

tile_size = 40 #size of each tile in pixels

#images for tiles
wall_img = pygame.image.load('Images/stone.png').convert_alpha()
mossy_wall_img = pygame.image.load('Images/mossystone.png').convert_alpha()
floor_img = pygame.image.load('Images/wood.png').convert_alpha()
floor2_img = pygame.image.load('Images/wood4.png').convert_alpha()

#door images
doorleft_img = pygame.image.load('Images/doors/doorleft.png').convert_alpha()
doorright_img = pygame.image.load('Images/doors/doorright.png').convert_alpha()
doortop_img = pygame.image.load('Images/doors/doortop.png').convert_alpha()
doorbottom_img = pygame.image.load('Images/doors/doorbottom.png').convert_alpha()

doorlockedleft_img = pygame.image.load('Images/doors/doorlockedleft.png').convert_alpha()
doorlockedright_img = pygame.image.load('Images/doors/doorlockedright.png').convert_alpha()
doorlockedtop_img = pygame.image.load('Images/doors/doorlockedtop.png').convert_alpha()
doorlockedbottom_img = pygame.image.load('Images/doors/doorlockedbottom.png').convert_alpha()


#scales images to tile size
wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))
mossy_wall_img = pygame.transform.scale(mossy_wall_img, (tile_size, tile_size))
floor_img = pygame.transform.scale(floor_img, (tile_size, tile_size))
floor2_img = pygame.transform.scale(floor2_img, (tile_size, tile_size))

#scale door images to tile size
doorleft_img = pygame.transform.scale(doorleft_img, (tile_size, tile_size))
doorright_img = pygame.transform.scale(doorright_img, (tile_size, tile_size))
doortop_img = pygame.transform.scale(doortop_img, (tile_size, tile_size))
doorbottom_img = pygame.transform.scale(doorbottom_img, (tile_size, tile_size))

doorlockedleft_img = pygame.transform.scale(doorlockedleft_img, (tile_size, tile_size))
doorlockedright_img = pygame.transform.scale(doorlockedright_img, (tile_size, tile_size))
doorlockedtop_img = pygame.transform.scale(doorlockedtop_img, (tile_size, tile_size))
doorlockedbottom_img = pygame.transform.scale(doorlockedbottom_img, (tile_size, tile_size))

#lists of tile variants for visual variety
wall_variants = [wall_img, mossy_wall_img]
floor_variants = [floor_img, floor2_img]

class room:
    def __init__(self, max_width, max_height, open_room = False):
        self.width = (random.randint(20, max_width))   #number of columns
        self.height = (random.randint(10, max_height))     #number of rows
        
        self.template = [[0 for _ in range(self.width)] for _ in range(self.height)]
        #Creates a 2D array (list of lists) to represent the room
        #room template initialized with all walls (0)
        
        self.variant = [[random.randint(0, len(wall_variants) - 1) if self.template[y][x] == wall #if tile is wall, assign a random wall variant index
                         else random.randint(0, len(floor_variants) - 1) if self.template[y][x] == floor #if tile is floor, assign a random floor variant index
                            else 0 #door variant (only 1 type of door)
                            for x in range(self.width)] for y in range(self.height)] #creates array to store the variant index for each tile
        
        for y in range(1, self.height -1): #leaves outer walls
            for x in range(1, self.width -1):
                
                if open_room:
                    self.template[y][x] = 1 #fully open floor
                
                else:
                    if random.random() < 0.9: #90% chance of being floor
                        self.template[y][x] = 1 #floor

        self.door_positions = self.add_door()
        self.remove_internal_walls_near_doors()
        
    #add door
    def add_door (self): #creates a 2 tile door
        #choose which wall door appears on
        side = random.choice (["top", "bottom", "left", "right"]) #randomly chooses a side for the door
        
        if side in ("top", "bottom"): #tuple for if the side selected is top/bottom
            #horizontal door
            x = random.randint(1, self.width - 3) #ensures x and x+1 aren't at corners by starting at 1     #adjuacent tiles
            y = 0 if side == "top" else self.height - 1 #depending on side chosen, y is set to 0 for top or -1 for bottom
            self.template [y][x] = 2 #tile is made to be door tile
            self.template [y][x + 1] = 2 #adjacent tile made to be door tile
            return [(x,y), (x + 1, y)] #returns positions of door tiles
        
        else:
            #vertical door
            x = 0 if side == "left" else self.width - 1 #depending on side, 0 = left, -1=right
            y = random.randint (1, self.height - 3) #ensures x and x+1 aren't at corners
            
            self.template[y][x] = 2 #tile made to be door tile
            self.template[y + 1][x] = 2 #adjacent tile made to be door tile
            return [(x, y), (x, y + 1)] #returns positions of door tiles
            
    def tiles(self):
        for ty in range(self.height):               #ty = tile y position in the room
            for tx in range(self.width):            #tx = tile x position in the room
                yield tx, ty, self.template[ty][tx] #yields the tile position and type
    
    #^shows all tile positions and types in the room^
    
    def floor_positions(self):
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.template[y][x] == 1: #if tile is floor
                    positions.append((x, y)) #add position to list
        return positions
    
    def remove_internal_walls_near_doors(self):
        for (dx, dy) in self.door_positions: #for door coordinates
            neighbours = [(dx + 1, dy), (dx - 1, dy), (dx, dy + 1), (dx, dy - 1)]
            
            for nx, ny in neighbours:
                #skip tiles outside room
                if not (0 <=nx < self.width and 0 <= ny < self.height): #checks if the tile is inside room
                    continue
                
                #skip outer border of walls
                if nx == 0 or ny == 0 or nx == self.width-1 or ny == self.height - 1: #if its a border wall tile
                    continue
                
                #change internal walls next to doors into floors
                if self.template [ny][nx] == 0: #if wall
                    self.template [ny][nx] = 1 #change to floor
    

def draw_room(room, screen, screen_width, screen_height, door_locked):
    
    walls = []
    doors = []
    
    #calculate pixel dimensions of the room
    room_pixel_width = room.width * tile_size
    room_pixel_height = room.height * tile_size
    
    #calculate offsets to center the room on the screen
    offset_x = (screen_width - room_pixel_width) // 2
    offset_y = (screen_height - room_pixel_height) // 2
    
    for tx, ty, tile in room.tiles():
        #build the rectangle
        px = tx * tile_size + offset_x
        py = ty * tile_size + offset_y
        
        if tile == wall: #if tile is wall
            walls.append(pygame.Rect(px, py, tile_size, tile_size)) #add wall rectangle to list
            index = room.variant[ty][tx] #get variant index for this tile
            screen.blit(wall_variants[index], (px, py)) #draw wall tile
        
        elif tile == floor: #if tile is floor
            index = room.variant[ty][tx] #get variant index for this tile
            screen.blit(floor_variants[index], (px, py)) #draw floor tile
            
            
        elif tile == door: #if tile is door
            doors.append(pygame.Rect(px, py, tile_size, tile_size)) #add door rectangle to list
            
            if door_locked:
                left_img = doorlockedleft_img
                right_img = doorlockedright_img
                top_img = doorlockedtop_img
                bottom_img = doorlockedbottom_img
                
            else:
                left_img = doorleft_img
                right_img = doorright_img
                top_img = doortop_img
                bottom_img = doorbottom_img
            
            #detect if horizontal
            if tx + 1 < room.width and room.template[ty][tx + 1] == door: #if the tile to the left is also a door tile
                screen.blit(left_img, (px, py)) #draw horizontal left door tile
                
            elif tx - 1 >= 0 and room.template[ty][tx - 1] == door: #if the tile to the right is also a door tile
                screen.blit(right_img, (px, py)) #draw horizontal right door tile
                
            #detect if vertical
            elif ty + 1 < room.height and room.template[ty + 1][tx] == door: #if the tile below is also a door tile
                screen.blit(top_img, (px, py)) #draw vertical top door tile
                
            elif ty - 1 >= 0 and room.template[ty - 1][tx] == door: #if the tile above is also a door tile
                screen.blit(bottom_img, (px, py)) #draw vertical bottom door tile
                
    return walls, doors

current_room = room(25, 15) #create initial room
