import pygame, random, Rooms, pathfinding, animations, health, math

pygame.mixer.init()
attack = pygame.mixer.Sound('Sounds/attack.mp3')

#enemy class
enemy_width = 40
enemy_height = 40

screen_width = 1200
screen_height = 750

class enemy(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_width, enemy_height) #enemy represented as a rectangle        
        self.max_health = 100
        self.health = self.max_health #initial health value set as max health

        #attacking animation
        self.attacking = False #whether enemy is currently attacking
        self.attack_duration = 300 #milliseconds attack animation lasts
        self.attack_start_time = 0 #time when attack animation started
        
        #attack
        self.damage = 5 #damage dealt to player on collision
        self.attack_cooldown = 1000 #milliseconds between attacks
        self.last_attack_time = 0 #time of last attack
        self.attack_range = 30 #distance within which enemy can attack player
        
        #movement
        self.direction = "down" #initial direction for animation purposes
        self.moving = False #initially not moving for animation purposes
        
        #death state
        self.dying = False          #playing death animation
        self.dead = False           #fully dead and should be removed from game
        self.death_start_time = 0   #time when death animation started
        self.death_duration = 500   #milliseconds death animation lasts
        
        #load animations for each direction
        self.animations = {
            "up": animations.Animation("Images/Animations/skeleton/skeletonmovement/skeletonup", scale=(40,40)),
            "down": animations.Animation("Images/Animations/skeleton/skeletonmovement/skeletondown", scale=(40,40)),
            "left": animations.Animation("Images/Animations/skeleton/skeletonmovement/skeletonleft", scale=(40,40)),
            "right": animations.Animation("Images/Animations/skeleton/skeletonmovement/skeletonright", scale=(40,40)),
            
            #attack animations
            "attack_up": animations.Animation("Images/Animations/skeleton/skeletonattack/attackup", scale=(40,40), frame_time=100),
            "attack_down": animations.Animation("Images/Animations/skeleton/skeletonattack/attackdown", scale=(40,40), frame_time=100),
            "attack_left": animations.Animation("Images/Animations/skeleton/skeletonattack/attackleft", scale=(40,40), frame_time=100),
            "attack_right": animations.Animation("Images/Animations/skeleton/skeletonattack/attackright", scale=(40,40), frame_time=100),
        
            #death animation
            "death": animations.Animation("Images/Animations/skeleton/skeletondeath", scale=(40,40), frame_time=100)
            
            
            }
        
        #pathfinding state
        self.path = [] #current A* path
        self.last_tile = None # last tile used to calculate path
        
def spawn_enemy():
    floor_tiles = Rooms.current_room.floor_positions() #creates list of floor tiles
    tile_x, tile_y = random.choice(floor_tiles) #choose random floor tile position

    #convert tile position to pixel position
    enemy_pixel_x = tile_x * Rooms.tile_size
    enemy_pixel_y = tile_y * Rooms.tile_size

    #calculate pixel dimensions of the room
    room_pixel_width = Rooms.current_room.width * Rooms.tile_size
    room_pixel_height = Rooms.current_room.height * Rooms.tile_size

    #calculate offsets of the room
    offset_x = (screen_width - room_pixel_width) // 2
    offset_y = (screen_height - room_pixel_height) // 2

    #added offsets to tile pixel position
    enemy_pixel_x += offset_x
    enemy_pixel_y += offset_y

    #creating enemy instances
    return enemy (enemy_pixel_x, enemy_pixel_y)


    

def pixel_to_tile (pixel_x, pixel_y, room): #function to convert pixel position to tile position
    
    #calculate offsets of the room
    offset_x = (screen_width - room.width * Rooms.tile_size) // 2
    offset_y = (screen_height - room.height * Rooms.tile_size) // 2
    
    #remove offsets from pixel position
    tile_x = (pixel_x - offset_x) // Rooms.tile_size
    tile_y = (pixel_y - offset_y) // Rooms.tile_size
    
    return (tile_x, tile_y) #returns tile position as a tuple



def tile_to_pixel (tile_x, tile_y, room): #function to convert tile position to pixel position
    
    #calculate offsets of the room
    offset_x = (screen_width - room.width * Rooms.tile_size) // 2
    offset_y = (screen_height - room.height * Rooms.tile_size) // 2
    
    #convert tile position to pixel position and add offsets
    pixel_x = tile_x * Rooms.tile_size + offset_x
    pixel_y = tile_y * Rooms.tile_size + offset_y
    
    return (pixel_x, pixel_y) #returns pixel position as a tuple


           
def move_enemy_pathfinding(enemy, player, room, walls, enemies, speed = 1): #create pathfinding function
    
    #store original position
    original_x = enemy.x
    original_y = enemy.y
    
    if enemy.attacking or enemy.dying or enemy.dead:
        return #do not move if currently attacking or dying or dead
            
    #convert enemy and player pixel positions to tile positions
    enemy_tile = pixel_to_tile(enemy.centerx, enemy.centery,room)
    player_tile = pixel_to_tile(player.rect.centerx, player.rect.centery, room)
    
    #get path from enemy to player using A* algorithm (list of tile positions)
    if enemy.last_tile != enemy_tile or not enemy.path:
        enemy.path = pathfinding.astar(room, enemy_tile, player_tile)
        enemy.last_tile = enemy_tile
    
    if not enemy.path: #if there is no path, do not move
        return #exit function
    
    #skip current tile if its the 1st step in the path
    if len(enemy.path)>1 and enemy.path[0] == enemy_tile:
        next_tile = enemy.path [1]
    else:
        next_tile = enemy.path[0]
    
    target_pixel = tile_to_pixel(next_tile[0], next_tile[1], room) #convert next tile position to pixel position
    target_x, target_y = target_pixel
        
    #move enemy towards target pixel position
    target_cx = target_x + enemy.width // 2 #calculate center x of target position
    target_cy = target_y + enemy.height // 2 #calculate center y of target
    
    distance_x = target_cx - enemy.centerx #calculate distance from enemy center to target center
    distance_y = target_cy - enemy.centery #calculate distance from enemy center to target center
    
    
    #diagonal speed fix
    if abs(distance_x) > speed and abs(distance_y) > speed:
        diag_scale = speed / math.sqrt(2)   # prevents the speed boost
    else:
        diag_scale = speed

    
    enemy.moving = False #reset moving status for animation purposes
    
    #move in x direction/horizontal movement
    if abs(distance_x) > speed: #if distance is greater than speed, move by speed
        enemy.x += diag_scale if distance_x > 0 else -diag_scale #move right if distance_x is positive, else move left
        enemy.direction = "right" if distance_x > 0 else "left" #set animation direction based on movement
        enemy.moving = True #set moving status for animation purposes
    else:
        if abs(distance_x) > 0: #if distance < speed > 0, move directly to target to prevent overshooting
            enemy.centerx = target_cx #move directly to target center x
    
    collided_x = any(enemy.colliderect(wall) for wall in walls)
    if collided_x:
        enemy.x = original_x
        
    #move in y direction/vertical movement
    if abs(distance_y) > speed: #if distance is greater than speed, move by speed
        enemy.y += diag_scale if distance_y > 0 else - diag_scale #move down if distance_y is positive, else move up
        enemy.direction = "down" if distance_y > 0 else "up" #set animation direction based on movement
        enemy.moving = True #set moving status for animation purposes
    else:
        if abs(distance_y) > 0: #if distance is less than speed but greater than 0, move directly to target to prevent overshooting
            enemy.centery = target_cy #move directly to target center y    

    collided_y = any(enemy.colliderect(wall) for wall in walls)
    if collided_y:
        enemy.y = original_y


    #collision detection----------------------------------------------
    if (collided_x or collided_y) and enemy.path:
        #remove blocked tile from pathfinding
        enemy.path.pop(0)
        enemy.path = pathfinding.astar(room, enemy_tile, player_tile)
                
    for other in enemies:
        if other is not enemy and enemy.colliderect(other): #checks for collision with other enemies
            
            #calculates distance from other enemy (tells which direction to move)
            distance_x = enemy.x - other.x #if enemy is to the right of other enemy, distance_x is positive
            distance_y = enemy.y - other.y #if enemy is below other enemy, distance_y is positive
            
            if distance_x == 0 and distance_y == 0: #if both enemies are in the exact same position
                #move in a random direction to separate them
                distance_x = random.choice([-1, 1])
                distance_y = random.choice([-1, 1])
                
            #normalize distance
            length = max(1, (distance_x*distance_x + distance_y*distance_y)**0.5) #prevents division by zero
            #keeps the distance the same but makes the length equal to 1
            distance_x /= length
            distance_y /= length
            
            #move enemy away from other enemy
            enemy.x += int(distance_x * 2) #move 2 pixels away
            enemy.y += int(distance_y * 2) #move 2 pixels away
            
    enemy_tile = pixel_to_tile(enemy.centerx, enemy.centery, room)
    
    if enemy.path and enemy_tile == enemy.path[0]:
        enemy.path.pop(0) #once enemy reaches a tile, it is removed from the list/not targeted anymore
            
    #enemy attack
    dist = math.dist((enemy.centerx, enemy.centery), (player.rect.centerx, player.rect.centery)) #calculate distance to player
    
    if dist <= enemy.attack_range + 10: #if player is within attack range                
        now = pygame.time.get_ticks()
        can_enemy_attack = now - enemy.last_attack_time >= enemy.attack_cooldown and not player.invincible #check if enough time has passed since last attack
        
        if can_enemy_attack:
            attack.play()
            #damage player
            health.apply_damage(enemy.damage)            
            #attack animation
            
            #set player invincibility
            player.start_invincibility(1000, (255,0,0)) #1 second of invincibility with red glow
            
            
            enemy.attacking = True
            enemy.attack_start_time = now #set attack start time for animation purposes
            enemy.last_attack_time = now #update time of last attack
            
            
def draw_enemy_health (screenGame, enemy):
    bar_width = enemy.width
    bar_height = 5
    bar_x = enemy.x
    bar_y = enemy.y - bar_height - 2 #position health bar above enemy with a small gap
    
    
    if enemy.health <= 0:
        health_ratio = 0
    else:
        health_ratio = enemy.health / enemy.max_health #calculate health ratio for scaling the health bar
    
    pygame.draw.rect(screenGame, "red", (bar_x, bar_y, bar_width, bar_height)) #draw background of health bar (red)
    pygame.draw.rect(screenGame, "green", (bar_x, bar_y, bar_width * health_ratio, bar_height)) #draw foreground of health bar (green) scaled by health ratio

def update_enemy_animation(enemy):
    now = pygame.time.get_ticks() #current time in milliseconds
    
    #death animation
    if enemy.dying:
        enemy.animations["death"].update() #update death animation frame
        
        #when animation finishes, mark enemy as fully dead
        if now - enemy.death_start_time >= enemy.death_duration: #if death animation duration has passed
            enemy.dying = False
            enemy.dead = True #mark enemy as fully dead after death animation finishes
        return #skip other animations if currently dying
    
    #attack animation
    if enemy.attacking:
        key = "attack_" + enemy.direction #get attack animation key based on current direction
        enemy.animations[key].update() #update attack animation frame
        
        #end attack animation after duration has passed
        if now - enemy.attack_start_time >= enemy.attack_duration:
            enemy.attacking = False #reset attacking status
        return #skip movement animation if attacking
    
    #movement animation
    current_animation = enemy.animations[enemy.direction] #get current animation based on enemy direction
    
    if enemy.moving:
        current_animation.update() #advance animation if enemy is moving
    else:
        current_animation.reset() #reset to idle frame if enemy is not moving
        
    