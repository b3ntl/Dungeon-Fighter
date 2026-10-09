import pygame , Button , settings_screen

pygame.init()

pygame.mixer.init()
click = pygame.mixer.Sound('Sounds/click.mp3')

#create display window
screen_width = 1200
screen_height = 750
screenV = pygame.display.set_mode((screen_width, screen_height)) #creates display screen

settings_img = pygame.image.load("Images/settings.png").convert_alpha()
background3_img = pygame.image.load('Images/background3.png').convert_alpha()

#create button instances
back_button = Button.button(0, 0, settings_img, 1.75)

#create slider instance
slider = Button.slider((0, 0), (600, 50), 0.5, 0, 100, 20)
                    #position, size, initial value (as percentage), min value, max value


#position buttons
screen_rect = screenV.get_rect()
back_button.rect.bottomright = (screen_rect.right - 30, screen_rect.bottom - 30) #position back button in the bottom right corner with some padding
slider.container_rect.center = (screen_rect.centerx, 300)  #position slider in the center of the screen

#internal slider positions
slider.slider_left_pos = slider.container_rect.left
slider.slider_right_pos = slider.container_rect.right
slider.slider_top_pos = slider.container_rect.top

handle_x = slider.slider_left_pos + slider.initial_val
handle_x = max(slider.slider_left_pos, min(slider.slider_right_pos, handle_x))  #clamp handle position within slider bounds
slider.button_rect.centerx = handle_x
slider.button_rect.centery = slider.container_rect.centery

screenV.fill((40, 40, 40)) #changes the screen background colour


background = pygame.transform.scale(background3_img, (screen_width, screen_height)) #scale background image to screen size
background_rect = background.get_rect(topleft = (0,0)) #position background to be central

def Vrun():
        global music_volume
    
        current_state = "volume_screen"
        pygame.display.set_caption('Volume Menu') #captions the display
        screenV.fill((40, 40, 40)) #changes the screen background colour

        screenV.blit(background, background_rect) #draw background image
        
        #gets mouse position and checks whether it's pressed
        mouse_pos = pygame.mouse.get_pos()  #gets mouse position
        mouse_pressed = pygame.mouse.get_pressed()[0]  #checks if mouse is pressed

        if slider.container_rect.collidepoint(pygame.mouse.get_pos()) and mouse_pressed:  #checks if mouse is over slider
            slider.move_slider(mouse_pos)
                
        slider.render(screenV) #draw slider
        
        font = pygame.font.SysFont('Arial', 50, bold=True) #leaderboard font
        volume_value = slider.getValue()  #gets current slider value
        volume_label = font.render(f'Volume: {int(volume_value)}', True, (255, 255, 255)) #renders volume text in white
        screenV.blit(volume_label, (screen_rect.centerx - volume_label.get_width() // 2, 350)) #positions volume text

        music_volume = max(0.0, min(1.0, volume_value / 100.0))
        pygame.mixer.music.set_volume(music_volume)
        click.set_volume(music_volume)

        if back_button.draw(screenV): #back button to main menu
            click.play()
            current_state = "settings_screen"
            pygame.time.delay(200) #delay to prevent multiple clicks
            return(current_state)                
                
        pygame.display.flip() #update the display        
                
        return "volume_screen"