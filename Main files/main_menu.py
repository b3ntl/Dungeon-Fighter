import pygame , Button, volume_screen


pygame.init()

pygame.mixer.init()
click = pygame.mixer.Sound('Sounds/click.mp3')
#click.set_volume(volume_screen.music_volume)


#create display window
screen_width = 1200
screen_height = 750
screenM = pygame.display.set_mode((screen_width, screen_height)) #creates display screen


#button images
play_img = pygame.image.load('Images/play.png').convert_alpha()
leaderboard_img = pygame.image.load('Images/leaderboard.png').convert_alpha()
settings_img = pygame.image.load('Images/settings.png').convert_alpha()
exit_img = pygame.image.load('Images/exit.png').convert_alpha()
background_img = pygame.image.load('Images/background.png').convert_alpha()
dungeon_img = pygame.image.load('Images/dungeonfighter.png').convert_alpha()

#create button instances
play_button = Button.button(0, 0, play_img, 1.75)
leaderboard_button = Button.button(0, 0, leaderboard_img, 1.75)
settings_button = Button.button(0, 0, settings_img, 1.75)
exit_button = Button.button(0, 0, exit_img, 1.75)
dungeon_button = Button.button(0, 0, dungeon_img, 0.45)

background = pygame.transform.scale(background_img, (screen_width, screen_height)) #scale background image to screen size
background_rect = background.get_rect(topleft = (0,0)) #position background to be central

#position buttons
start_y = 330 #initial y position for the first button
spacing = 100 #spacing between buttons

screen_rect = screenM.get_rect()

play_button.rect.centerx = screen_rect.centerx
leaderboard_button.rect.centerx = screen_rect.centerx
settings_button.rect.centerx = screen_rect.centerx
dungeon_button.rect.centerx = screen_rect.centerx

play_button.rect.centery = start_y
leaderboard_button.rect.centery = start_y + 1 * spacing
settings_button.rect.centery = start_y + 2 * spacing

dungeon_button.rect.centery = start_y - 175 #position dungeon fighter image above the buttons

exit_button.rect.bottomright = (screen_rect.right - 30, screen_rect.bottom - 30) #position exit button in the bottom right corner with some padding

def Mrun():
        current_state = "main_menu"
        pygame.display.set_caption('Start Menu') #captions the display
        screenM.fill((40, 40, 40)) #changes the screen background colour
        
        screenM.blit(background, background_rect) #draw background image
        
        dungeon_button.draw(screenM) #draw dungeon fighter image
        
        if play_button.draw(screenM):
                click.play()
                current_state = "game"
                pygame.time.delay(200) #delay to prevent multiple clicks
                return(current_state)
                
        if leaderboard_button.draw(screenM):
                click.play()
                current_state = "leaderboard_screen"
                pygame.time.delay(200) #delay to prevent multiple clicks
                return(current_state)
                
        if settings_button.draw(screenM):
                click.play()
                current_state = "settings_screen"
                pygame.time.delay(200) #delay to prevent multiple clicks
                return(current_state)
                
        if exit_button.draw(screenM):
                click.play()
                current_state = "exit"
                return(current_state)
        
                
        #event loop for main menu       
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        current_state = "exit"
                        return(current_state)
                
        pygame.display.flip() #updates the game window
        
        return "main_menu"