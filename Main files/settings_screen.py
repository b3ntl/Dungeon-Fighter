import pygame , Button, volume_screen

pygame.init()

pygame.mixer.init()
click = pygame.mixer.Sound('Sounds/click.mp3')
#click.set_volume(volume_screen.music_volume)

#create display window
screen_width = 1200
screen_height = 750
screenS = pygame.display.set_mode((screen_width, screen_height)) #creates display screen

#load images
mainmenu_img = pygame.image.load("Images/mainmenu.png").convert_alpha()
background3_img = pygame.image.load('Images/background3.png').convert_alpha()
volume_img = pygame.image.load('Images/volume.png').convert_alpha()
keybinds_img = pygame.image.load('Images/keybinds.png').convert_alpha()

#create button instances
back_button = Button.button(0, 0, mainmenu_img, 1.75)
volume_button = Button.button(0, 0, volume_img, 1.75)
keybinds_button = Button.button(0, 0, keybinds_img, 1.75)

#background
background = pygame.transform.scale(background3_img, (screen_width, screen_height)) #scale background image to screen size
background_rect = background.get_rect(topleft = (0,0)) #position background to be central

#position buttons
start_y = 290 #initial y position for the first button
spacing = 180 #spacing between buttons

screen_rect = screenS.get_rect()
volume_button.rect.centerx = screen_rect.centerx
keybinds_button.rect.centerx = screen_rect.centerx

volume_button.rect.centery = start_y
keybinds_button.rect.centery = start_y + 1 * spacing

back_button.rect.bottomright = (screen_rect.right - 30, screen_rect.bottom - 30) #position back button in the bottom right corner with some padding

def Srun():
        current_state = "settings_screen"
        pygame.display.set_caption('Settings Menu') #captions the display
        screenS.fill((40, 40, 40)) #changes the screen background colour

        screenS.blit(background, background_rect) #draw background image


        if back_button.draw(screenS): #back button to main menu
            click.play()
            current_state = "main_menu"
            pygame.time.delay(200) #delay to prevent multiple clicks
            return(current_state)
        
        if volume_button.draw(screenS): #volume settings button
            click.play()
            current_state = "volume_screen"
            pygame.time.delay(200) #delay to prevent multiple clicks
            return(current_state)
        
        if keybinds_button.draw(screenS): #keybinds settings button
            click.play()
            current_state = "keybinds_screen"
            pygame.time.delay(200) #delay to prevent multiple clicks
            return(current_state)
        
            
        
        return "settings_screen"