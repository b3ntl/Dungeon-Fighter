import pygame, animations, math, Rooms, keybinds, inventory

pygame.mixer.init()
sword = pygame.mixer.Sound('Sounds/sword.mp3')

class Player:
    def __init__ (self, x, y):
        
        #position + colision box
        self.rect = pygame.Rect(x, y, 40, 40)
        
        #movement values
        self.speed = 5  #how fast per frame
        self.move_x = 0 #initial x movement
        self.move_y = 0 #initial y movement
        
        #player direction
        self.direction = "down" #start direction
        
        #check if player is moving
        self.moving = False
        
        #Attacking
        self.attacking = False
        self.attack_cooldown = 500 #milliseconds between attacks
        self.attack_duration = 200 #milliseconds attack animation lasts
        self.last_attack_time = 0 #time of last attack
        self.attack_rect = None #rectangle representing attack hitbox
        
        self.attack_damage = 25 #damage dealt by attack
        self.attack_knockback = 10 #knockback applied to enemies hit by attack
        
        #invincibility
        self.invincible = False
        self.invincibility_duration = 0 #how long invincibility lasts in milliseconds
        self.invincibility_start_time = 0 #time when invincibility started
        
        #glow settings
        self.glow_color = (0,255,255) #color of glow when invincible
        self.glow_max_alpha = 150 #how strong glow gets
        self.glow_min_alpha = 50 #minimum glow strength
        self.glow_pulse_speed = 0.008 #how fast glow pulses
        self.glow_extra_radius = 10 #how far glow extends beyond player
        
        #inventory
        self.inventory = inventory.Inventory()
            
        #ANIMATIONS--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        #load animations for each direction
        self.animations = {
            "up": animations.Animation("Images/Animations/knight/knightup", scale=(40,40), frame_time=50),
            "down": animations.Animation("Images/Animations/knight/knightdown", scale=(40,40), frame_time=50),
            "left": animations.Animation("Images/Animations/knight/knightleft", scale=(40,40), frame_time=50),
            "right": animations.Animation("Images/Animations/knight/knightright", scale=(40,40), frame_time=50),
        
        #attack animations
            "attack_up": animations.Animation("Images/Animations/knight/attackup", scale=(40,40), frame_time=100),
            "attack_down": animations.Animation("Images/Animations/knight/attackdown", scale=(40,40), frame_time=100),
            "attack_left": animations.Animation("Images/Animations/knight/attackleft", scale=(40,40), frame_time=100),
            "attack_right": animations.Animation("Images/Animations/knight/attackright", scale=(40,40), frame_time=100)
        
        }
        
    def start_invincibility(self, duration, glow_color):
        #invinsibility after being hit
        self.invincible = True
        self.invincibility_duration = duration #milliseconds of invincibility after being hit
        self.invincibility_start_time = pygame.time.get_ticks() #time when invincibility started
        
        if glow_color is not None:
            self.glow_color = glow_color
    
    #checks keyboard input    
    def handle_input (self, keys, mouse_buttons = None):
        if mouse_buttons is None:
            mouse_buttons = pygame.mouse.get_pressed()
        
        #attack input
        if self.attacking:
            self.move_x = self.move_y = 0 #stop movement while attacking
            return #skip movement input if currently attacking
        
        #movement input
        #resets movement after each frame to prevent continuos movement
        self.move_x = 0
        self.move_y = 0
        self.moving = False
        
            #left movement
        if keys[keybinds.keybinds["move_left"]]: #move left if left key is pressed
            self.move_x -= self.speed
            self.direction = "left"
            self.moving = True
            
        #right movement
        if keys[keybinds.keybinds["move_right"]]: #move right if 'D' key is pressed
            self.move_x += self.speed
            self.direction = "right"
            self.moving = True
            
        #up movement
        if keys[keybinds.keybinds["move_up"]]: #move up if 'W' key is pressed
            self.move_y -= self.speed
            self.direction = "up"
            self.moving = True
        
        #down movement
        if keys[keybinds.keybinds["move_down"]]: #move down if 'S' key is pressed
            self.move_y += self.speed
            self.direction = "down"
            self.moving = True
        
            
    def move (self, solid_tiles): #moves player + resolves collisions
        
        #horizontal movement
        self.rect.x += self.move_x
        for tile in solid_tiles:
            if self.rect.colliderect(tile): #if colliding
                if self.move_x > 0:
                    self.rect.right = tile.left #if moving right, snap player to tile's left edge
                elif self.move_x < 0:
                    self.rect.left = tile.right #if moving left, snap player to tile's right edge
        
        #vertical movement            
        self.rect.y += self.move_y
        for tile in solid_tiles:
            if self.rect.colliderect(tile): #if colliding
                if self.move_y > 0:
                    self.rect.bottom = tile.top #if moving down, snap player to top of tile
                elif self.move_y < 0:
                    self.rect.top = tile.bottom #if moving up, snap player to bottom of tile
    
    def calculate_attack_hitbox(self):
        w, h = self.rect.width, self.rect.height
        forward = 20 #how far attack hitbox extends in front of player
        side = 12 #how far attack hitbox extends to sides of player
        back_overlap = 20
        
        #calculate attack hitbox based on player direction
        if self.direction == "up":
            hit_h = forward + back_overlap
            top = self.rect.top - forward
            left = self.rect.centerx - (w // 2) - side
            return pygame.Rect(left, top, w + side * 2, hit_h)
        
        if  self.direction == "down":
            hit_h = forward + back_overlap
            top = self.rect.bottom - back_overlap
            left = self.rect.centerx - (w // 2) - side
            return pygame.Rect(left, top, w + side * 2, hit_h)

        if self.direction == "left":
            hit_w = forward + back_overlap
            left = self.rect.left - forward
            top = self.rect.centery - (h // 2) - side
            return pygame.Rect(left, top, hit_w, h + side * 2)

        if self.direction == "right":
            hit_w = forward + back_overlap
            left = self.rect.right - back_overlap
            top = self.rect.centery - (h // 2) - side
            return pygame.Rect(left, top, hit_w, h + side * 2)

    def start_attack(self, enemies_list):
        now = pygame.time.get_ticks()
        
        if now - self.last_attack_time < self.attack_cooldown: #if enough time has passed since last attack
            return
        
        sword.play() #sword sound
        
        self.last_attack_time = now
        self.attacking = True
        self.attack_rect = self.calculate_attack_hitbox() #calculate attack hitbox based on current position and direction
        
        #damage enemies in attack hitbox
        for e in enemies_list:
            if e.health > 0 and self.attack_rect.colliderect(e):
                e.health = max(0, e.health - self.attack_damage) #reduce enemy health by attack damage, but not below 0
                
                #knockback
                dx = e.centerx - self.rect.centerx #horizontal distance between player and enemy
                dy = e.centery - self.rect.centery #vertical distance between player and enemy
                length = max(1, (dx**2 + dy**2) ** 0.5) #distance between player and enemy, prevent division by zero

                #calculate knockback
                knock_x = int(self.attack_knockback * dx / length) #apply horizontal knockback based on distance
                knock_y = int(self.attack_knockback * dy / length) #apply vertical knockback based on distance
                
                #horizontal knockback
                e.x += knock_x
                if any (e.colliderect(wall) for wall in Rooms.walls):
                    e.x -= knock_x #undo horizontal move if blocked
                    
                #vertical knockback
                e.y += knock_y
                if any (e.colliderect(wall) for wall in Rooms.walls):
                    e.y -= knock_y #undo vertical move if blocked
                    
                
                #trigger death if enemy health reaches 0
                if e.health == 0 and not e.dying and not e.dead:
                    e.dying = True
                    e.attacking = False #stop enemy attack if currently attacking
                    
                    #whilst dying
                    e.moving = False #stop enemy movement
                    e.death_start_time = pygame.time.get_ticks() #record time when death animation starts
                                    
    def update_attack(self):
        if not self.attacking:
            return
        
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_duration: #if attack duration has passed
            self.attacking = False
            self.attack_rect = None #remove attack hitbox
            
    def update_invincibility(self):
        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.invincibility_start_time >= self.invincibility_duration: #if invincibility duration has passed
                self.invincible = False
    
    def draw_glow(self, screen):
        base_radius = max(self.rect.width, self.rect.height) // 2 + self.glow_extra_radius #base radius of glow based on player size
        t = pygame.time.get_ticks()
        pulse = (math.sin(t * self.glow_pulse_speed) + 1) / 2 #calculate pulse value between 0 and 1
        alpha = int(self.glow_min_alpha + pulse * (self.glow_max_alpha - self.glow_min_alpha)) #calculate current alpha based on pulse
        
        #small transparent surface to draw glow on
        glow_size = (base_radius * 2 + 4, base_radius * 2 + 4) #size of glow surface        
        glow_surface = pygame.Surface(glow_size, pygame.SRCALPHA) #create transparent surface for glow
        
        #draw the glow as a circle on the glow surface
        center = (glow_size[0] // 2, glow_size[1] // 2)
        colour_with_alpha = (*self.glow_color, alpha) #color with current alpha
        pygame.draw.circle(glow_surface, colour_with_alpha, center, base_radius) #draw glow circle on glow surface
        
        #position to glow surface so that glow is centered on player
        glow_pos = (self.rect.centerx - center[0], self.rect.centery - center[1])
        screen.blit(glow_surface, glow_pos) #draw glow surface on main screen at calculated        
                
    #update animation frames based on movement                    
    def update_animation(self):
        
        #attacking animation
        if self.attacking:
            key = "attack_" + self.direction #get attack animation key based on current direction
            self.animations[key].update() #update attack animation frame
            return
        
        #choose animation relating to direction
        current_animation = self.animations[self.direction]
        
        #advances animation when moving
        if self.moving:
            current_animation.update()
        
        #shows idle frame when stopped
        else:
            current_animation.reset()
        
        
    
    #draw player on to screen        
    def draw (self, screen):
        
        if self.invincible:
            self.draw_glow(screen) #draw glow if currently invincible
        
        if self.attacking:
            image = self.animations["attack_" + self.direction].get_image() #get current attack animation frame based on direction
        else:
            image = self.animations[self.direction].get_image() #gets current animation frame
        screen.blit(image, self.rect)   #draw image at players position
        