import pygame, Rooms, enemies, health, player, Button, keybinds, items, random, inventory, volume_screen
from player import Player

pygame.init() #initializes pygame modules

#sounds
pygame.mixer.init()
click = pygame.mixer.Sound('Sounds/click.mp3')
enemydeath = pygame.mixer.Sound('Sounds/enemydeath.mp3')
doorunlock = pygame.mixer.Sound('Sounds/doorunlock.mp3')

#click.set_volume(volume_screen.music_volume)
#enemydeath.set_volume(volume_screen.music_volume)
#doorunlock.set_volume(volume_screen.music_volume)

#music
pygame.mixer.music.load('Sounds/backgroundmusic.mp3')
pygame.mixer.music.play(-1)

door_locked = True
Rooms.doors = []

#dropped items list
dropped_items = []
screen_width = 1200
screen_height = 750
screenGame = pygame.display.set_mode((screen_width, screen_height)) #creates display screen

paused = False

enemy_damage = 5
enemy_speed = 1

#score system
score = 0 #initialize score variable
def reset_score():
    global score
    score = 0

def reset_game():
    
    #room number
    global room_number, enemy_damage, enemy_speed
    room_number = 1

    #reset score
    reset_score()
    
    #reset player health
    health.health_bar.health = health.health_bar.max_health
    
    #reset armour
    health.shield_bar.shield = 0
    
    #reset player position
    player.rect.center = (screen_width // 2, screen_height // 2)
    
    #reset door state
    global door_locked
    door_locked = True
    
    #reset room
    Rooms.current_room = Rooms.room(25,15)
    
    #pause state
    global paused
    paused = False
    
    #reset enemies
    global enemies_list
    enemy_count = 10 if room_number % 5 == 0 else 5 #for every 5th room, spawn 10 enemies, else spawn 5
    enemies_list = [enemies.spawn_enemy() for _ in range (enemy_count)] #creates 5 enemies
    
    enemy_damage = 5
    enemy_speed = 1

    #reset player invincibility
    player.invincible = False
    
    #reset items
    dropped_items.clear()
    player.inventory.items.clear()
    

    

background_img = pygame.image.load('Images/background5.png').convert_alpha()
background = pygame.transform.scale(background_img, (screen_width, screen_height)) #scale background image to screen size
background_rect = background.get_rect(topleft = (0,0)) #position background to be central

#button setup
resume_img = pygame.image.load('Images/resume.png').convert_alpha()
exit_img = pygame.image.load('Images/exit.png').convert_alpha()
mainmenu_img = pygame.image.load('Images/mainmenu.png').convert_alpha()

scale = 1.5

resume_button = Button.button (0,0,resume_img, scale) #resume button object
exit_button = Button.button(0,0, exit_img, scale) #quit button object
mainmenu_button = Button.button(0,0, mainmenu_img, scale) #main menu button object

screen_rect = screenGame.get_rect() #get screen rectangle for centering buttons
resume_button.rect.midtop = (screen_rect.centerx, 250) #position resume button at top center of screen
mainmenu_button.rect.midtop = (screen_rect.centerx, 350) #position main menu button
exit_button.rect.midtop = (screen_rect.centerx, 450) #position quit button below resume button

#player setup
player = Player(screen_width // 2, screen_height //2) #spawns player in the centre

#enemy setup
enemies_list = []
for _ in range(5):  #spawn 5 enemies
    enemies_list.append(enemies.spawn_enemy())


#Enemy creation--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#creates enemy images
def draw_enemy(screenGame, enemy):
    
    if enemy.dying:
        img = enemy.animations["death"].get_image() #get current death animation frame
        screenGame.blit(img, enemy) #draw enemy on screen at its rectangle position
        return #skip other animations if currently dying
        
    if enemy.dead:
        return #do not draw if fully dead
    
    if enemy.attacking:
        img = enemy.animations["attack_" + enemy.direction].get_image() #get current attack animation frame based on enemy direction
    else:
        img = enemy.animations[enemy.direction].get_image() #get current animation frame based on enemy direction
    
    screenGame.blit(img, enemy) #draw enemy on screen at its rectangle position

#pause menu--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def draw_pause_menu(screen):
    
    #transparent overlay
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA) #create a surface for the overlay with alpha channel
    overlay.fill((0, 0, 0, 200)) #transparent black color (last value is alpha for transparency)
    screen.blit(overlay, (0, 0)) #draw overlay on screen
    
    #fonts and buttons for pause menu
    pause_font = pygame.font.SysFont('Arial', 60, bold=True) #font for pause menu
    
    #pause text
    label = pause_font.render("Paused", True, (255, 255, 255)) #render "Paused" text in white
    screen.blit(label, (screen_width // 2 - label.get_width() // 2, 150)) #position "Paused" text at top center
    
    #draw buttons
    if resume_button.draw(screen): #if resume button is clicked
        click.play()
        return "resume"
    
    if mainmenu_button.draw(screen):
        click.play()
        return "main_menu"
    
    if exit_button.draw(screen):    #if quit button is clicked
        click.play()
        pygame.quit() #quit pygame
        exit() #exit program
        
    return None #return None if no button was clicked
    
#GAME LOOP ----------------------------------------------------------------------------------------------------------------
def gameRun():
    
    pygame.display.set_caption('Dungeon Fighter') #captions the display
    

    #global variables to be used in game loop
    global paused, door_locked, enemies_list, score, enemy_damage, enemy_speed, room_number
    
    pygame.time.delay(20) #delay to control frame rate/doesn't run too fast
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "exit" #return exit state to main loop to quit game
            
        #pause functionality
        if event.type == pygame.KEYDOWN: #check for key press events
            if event.key == pygame.K_ESCAPE: #if escape key is pressed
                paused = not paused #toggle pause state

        #item useage
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_5:   #if user presses 1-5
                slot = event.key - pygame.K_1 #gains slot of number pressed
                player.inventory.use_item(slot, player) #item used
        
        
    #input        
    keys = pygame.key.get_pressed() #checks which keys are being pressed
    mouse_buttons = pygame.mouse.get_pressed()
    player.handle_input(keys, mouse_buttons) #calls handle input function   
    
    
#Drawing--------------------------------------------------------------------------
    
    #draw background
    screenGame.blit(background, background_rect) #draw background on screen
    
    #draw room and background
    screenGame.blit(background, background_rect) #draw background on screen
    Rooms.walls, Rooms.doors = Rooms.draw_room(Rooms.current_room, screenGame, screen_width, screen_height, door_locked) #update wall positions list
    
    #player drawing
    player.update_animation()
    player.draw (screenGame)        
    
    #draw health bar
    health.health_bar.draw_health(screenGame)
    font = pygame.font.SysFont('Arial', 30, bold=True) #leaderboard font
    health_text = f"Health: {health.health_bar.health}" #health text to display
    health_label = font.render(health_text, True, (255, 255, 255)) #renders health text in white
    screenGame.blit(health_label, (health.health_bar.x, health.health_bar.y - 30)) #positions health text

    
    # draw shield bar
    health.shield_bar.draw_shield(screenGame)
    # shield text
    shield_font = pygame.font.SysFont('Arial', 30, bold=True)
    shield_text = f"Armour: {health.shield_bar.shield}"
    shield_label = shield_font.render(shield_text, True, (0, 150, 255))
    screenGame.blit(shield_label, (health.shield_bar.x, health.shield_bar.y - 30))
    
    #score display
    font = pygame.font.SysFont('Arial', 30, bold=True) #score font
    score_text = f"Score: {score}" #score text to display
    score_label = font.render(score_text, True, (255, 255, 255)) #renders score text in white
    screenGame.blit(score_label, (screen_width - score_label.get_width() - 20, 10)) #positions score text at top right corner with some padding
    
    #inventory display
    inv_title_font = pygame.font.SysFont("Arial", 24, bold=True)    #inventory font
    inv_title = inv_title_font.render("Inventory:", True, (255, 255, 255))  #inventory title display
    screenGame.blit(inv_title, (20, 20))    #title drawing
    
    font = pygame.font.SysFont("Arial", 20) #font
    for i, item in enumerate(player.inventory.items):   #enumerate function turns list into pairs (index, value)
        text = font.render(f"{i+1}: {item.name}", True, (255,255,255)) #text of index no. & item name
        screenGame.blit(text, (20, 50 + i * 25))    #x pos, y pos, 25 y pos buffer
    
    #room number display
    room_font = pygame.font.SysFont("Arial", 24, bold=True)
    
    if room_number % 5 == 0:
        room_text = room_font.render(f"Room: {room_number} (Skeleton Wave)", True, (255,255,255))
    else:
        room_text = room_font.render(f"Room: {room_number}", True, (255,255,255))

    # position below inventory
    room_y = 50 + len(player.inventory.items) * 25 + 10
    screenGame.blit(room_text, (20, room_y))

    
    #handle pause state
    if paused:
        
        for e in enemies_list: #if paused, still draw enemies but do not update their movement or animations
            draw_enemy(screenGame, e)
            enemies.draw_enemy_health(screenGame, e)
        
        result = draw_pause_menu(screenGame) #draws pause menu

        
        if result == "resume":
            paused = False #resume game if resume button is clicked
            
        if result == "main_menu":
            return "main_menu"
            
        pygame.display.update() #update display to show pause menu
        return "game" #return game state to main loop to continue game loop
            
    #enemies code     
    if not paused:               
        for e in enemies_list[:]: #iterate over a copy of the list to allow for removal of dead enemies
            
            #enemy damage
            e.damage = enemy_damage
            
            
            #health
            if e.dead:
                enemydeath.play()
                
                if room_number % 5 == 0: #if 5th room, double score
                    score += 20
                else:
                    score += 10 #add 10 points to score for killing an enemy
                
                #random item drop
                drop_chance = random.random()
                
                if drop_chance <0.20: #20% chance
                    
                    roll = random.random()
                    if roll < 0.40:
                        # 40% = health potion
                        dropped_items.append(
                            items.create_health_potion(e.centerx, e.centery)
                        )
                    elif roll < 0.70:
                        # 30% = shield
                        dropped_items.append(
                            items.create_shield(e.centerx, e.centery)
                        )
                    else:
                        # 30% = armour
                        dropped_items.append(
                            items.create_armour(e.centerx, e.centery)
                        )

                
                enemies_list.remove(e) #remove fully dead enemies from the game
                continue #skip dead enemies
            
            #pathfinding, animation, and drawing
            enemies.move_enemy_pathfinding(e, player, Rooms.current_room, Rooms.walls, enemies_list, speed = enemy_speed)
            enemies.update_enemy_animation(e) #update enemy animation based on movement
            draw_enemy(screenGame, e) #draws enemy on screen
            enemies.draw_enemy_health(screenGame, e) #draws enemy health bar
    
    #item picking up
    for item in dropped_items[:]:
        item.draw(screenGame)
        
        if player.rect.colliderect(item.rect): #if player collides with item
            if player.inventory.add_item(item): #if player can add item to inventory
                dropped_items.remove(item) #pick up item from floor
    
    #solid tiles
    if door_locked:
        solid_tiles = Rooms.walls + Rooms.doors
    else:
        solid_tiles = Rooms.walls
    
    #player movement
    player.move(solid_tiles) #calls movement function with collisions    
    
    mouse_buttons = pygame.mouse.get_pressed()
    #player attack
    if keybinds.keybinds["attack"] == "mouse": #if space key is pressed
        if mouse_buttons[0]: #left click
            player.start_attack(enemies_list) #start attack and damage enemies in hitbox if possible
    else:
        if keys[keybinds.keybinds["attack"]]:
            player.start_attack(enemies_list)
    player.update_attack() #update attack animation frames
    
    #update player invincibility frames
    player.update_invincibility()
                    
    if not door_locked:
        for door in Rooms.doors:
            if player.rect.colliderect(door):
                
                doorunlock.play()
                
                room_number += 1
                
                #increase enemy damage by 1
                enemy_damage = min(enemy_damage + 1, 15)
                
                #increase speed
                enemy_speed = min(enemy_speed + 0.05, 2.5)
                
                #clear dropped items
                dropped_items.clear()
                
                #create new room
                wave_room = (room_number % 5 == 0) #wave rooms every 5th room
                Rooms.current_room = Rooms.room(25,15, open_room=wave_room)
                
                #respawn enemies
                enemy_count = 10 if room_number % 5 == 0 else 5 #for every 5th room, spawn 10 enemies, else spawn 5
                enemies_list = [enemies.spawn_enemy() for _ in range (enemy_count)] #creates enemies
                
                #lock new room's door
                door_locked = True
                
                #move player to center of screen
                player.rect.center = (screen_width // 2, screen_height // 2)
                
                #add temporary invincibility + glow
                player.start_invincibility(2000, (0,255,255)) #2 seconds of invincibility with cyan glow
                
    #door locking
    if door_locked and all(e.health <= 0 for e in enemies_list): #if the door is locked and all the enemies are dead
        door_locked = False #unlock door
    
    if health.health_bar.health <= 0: #if player health is 0 or less
        return "death_screen" #return death screen state to main loop to go to death screen
    
        
    pygame.display.update() #updates the game window
    
                                
    return "game" #return game state to main loop to continue game loop