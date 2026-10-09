import pygame , Button , volume_screen, keybinds

pygame.init()

pygame.mixer.init()
click = pygame.mixer.Sound('Sounds/click.mp3')
#click.set_volume(volume_screen.music_volume)

#create display window
screen_width = 1200
screen_height = 750
screenK = pygame.display.set_mode((screen_width, screen_height)) #creates display screen

settings_img = pygame.image.load("Images/settings.png").convert_alpha()
background3_img = pygame.image.load('Images/background3.png').convert_alpha()

#checkbox images
checkbox_on = pygame.image.load("Images/checkboxticked.png").convert_alpha()
checkbox_off = pygame.image.load("Images/checkbox.png").convert_alpha()

#font
font = pygame.font.SysFont('Arial', 40, bold=True)

#movement labels
wasd_label = font.render("WASD Movement", True, (255,255,255))
arrows_label = font.render("Arrow Key Movement", True, (255,255,255))

#attack labels
space_label = font.render("Space Attack", True, (255,255,255))
mouse_label = font.render("Left Click Attack", True, (255,255,255))


#scale checkbox
checkbox_scale = 1
checkbox_on = pygame.transform.scale(checkbox_on, (int(checkbox_on.get_width()*checkbox_scale),
                                                   int(checkbox_on.get_height()*checkbox_scale)))

checkbox_off = pygame.transform.scale(checkbox_off, (int(checkbox_off.get_width()*checkbox_scale),
                                                    int(checkbox_off.get_height()*checkbox_scale)))

#create button instances
back_button = Button.button(0, 0, settings_img, 1.75)

#position buttons
screen_rect = screenK.get_rect()
back_button.rect.bottomright = (screen_rect.right - 30, screen_rect.bottom - 30) #position back button in the bottom right corner with some padding

background = pygame.transform.scale(background3_img, (screen_width, screen_height)) #scale background image to screen size
background_rect = background.get_rect(topleft = (0,0)) #position background to be central


#layout/positions
checkbox_x = 80
label_x = 200
row_spacing = 70
movement_y = 200 
attack_y = 360       

# Create checkbox buttons
wasd_button   = Button.button(checkbox_x,movement_y + 0*row_spacing, checkbox_off, 1.0)
arrows_button = Button.button(checkbox_x,movement_y + 1*row_spacing, checkbox_off, 1.0)
space_button  = Button.button(checkbox_x,attack_y + 0*row_spacing, checkbox_off, 1.0)
mouse_button  = Button.button(checkbox_x,attack_y + 1*row_spacing, checkbox_off, 1.0)

def sync_checkbox_images_from_keybinds():
    using_wasd  = (keybinds.keybinds["move_up"] == pygame.K_w)
    using_space = (keybinds.keybinds["attack"] == pygame.K_SPACE)

    # Movement group
    wasd_button.image   = checkbox_on  if using_wasd else checkbox_off
    arrows_button.image = checkbox_on  if not using_wasd else checkbox_off

    # Attack group
    space_button.image  = checkbox_on  if using_space else checkbox_off
    mouse_button.image  = checkbox_on  if not using_space else checkbox_off

# Initial sync
sync_checkbox_images_from_keybinds()

def Krun():
    current_state = "keybinds_screen"
    screenK.blit(background, background_rect)
    pygame.display.set_caption('Keybinds Menu') #captions the display


    # Back
    if back_button.draw(screenK):
        click.play()
        pygame.time.delay(150)
        return "settings_screen"

    # Draw labels next to checkboxes
    screenK.blit(wasd_label,   (label_x, movement_y + 0*row_spacing))
    screenK.blit(arrows_label, (label_x, movement_y + 1*row_spacing))
    screenK.blit(space_label,  (label_x, attack_y + 0*row_spacing))
    screenK.blit(mouse_label,  (label_x, attack_y + 1*row_spacing))

    # Draw the checkbox buttons (and detect clicks)
    if wasd_button.draw(screenK):
        click.play()
        keybinds.set_wasd()
        sync_checkbox_images_from_keybinds()
        pygame.time.delay(120)

    if arrows_button.draw(screenK):
        click.play()
        keybinds.set_arrows()
        sync_checkbox_images_from_keybinds()
        pygame.time.delay(120)

    if space_button.draw(screenK):
        click.play()
        keybinds.set_attack_space()
        sync_checkbox_images_from_keybinds()
        pygame.time.delay(120)

    if mouse_button.draw(screenK):
        click.play()
        keybinds.set_attack_mouse()
        sync_checkbox_images_from_keybinds()
        pygame.time.delay(120)

    pygame.display.update()
    return current_state

