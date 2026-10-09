import pygame , Button , volume_screen, json

pygame.init()

pygame.mixer.init()
click = pygame.mixer.Sound('Sounds/click.mp3')
#click.set_volume(volume_screen.music_volume)

#create display window
screen_width = 1200
screen_height = 750
screenL = pygame.display.set_mode((screen_width, screen_height)) #creates display screen

mainmenu_img = pygame.image.load("Images/mainmenu.png").convert_alpha()
background2_img = pygame.image.load('Images/background2.png').convert_alpha()

#create button instances
back_button = Button.button(600, 430, mainmenu_img, 1.75)

#position buttons
screen_rect = screenL.get_rect()
back_button.rect.bottomright = (screen_rect.right - 30, screen_rect.bottom - 30) #position back button in the bottom right corner with some padding

background = pygame.transform.scale(background2_img, (screen_width, screen_height)) #scale background image to screen size
background_rect = background.get_rect(topleft = (0,0)) #position background to be central

def load_leaderboard():
    with open('leaderboard.json', 'r') as f: #opens leaderboard json file as a read only file
        leaderboard_data = json.load(f)
    return leaderboard_data

def Lrun():
        current_state = "leaderboard_screen"
        pygame.display.set_caption('Leaderboard Menu') #captions the display
        screenL.fill((40, 40, 40)) #changes the screen background colour

        screenL.blit(background, background_rect) #draw background image

        leaderboard = load_leaderboard() #loads leaderboard data from json file
        
        leaderboard = sorted(leaderboard, key=lambda x: x['Score'], reverse=True)[:10] #sorts leaderboard by score in descending order and takes top 10 entries
        
        font = pygame.font.SysFont('Arial', 50) #leaderboard font
        y_offset = 100 #vertical position
        
        #render leaderboard title
        title_font = pygame.font.SysFont('Arial', 64, bold=True)
        title_surf = title_font.render("Leaderboard", True, (255, 255, 255))
        title_x = screen_rect.centerx - title_surf.get_width() // 2
        title_y = 30
        screenL.blit(title_surf, (title_x, title_y))

        
        for entry in leaderboard: #loop for each entry in the leaderboard
            text = f"{entry['Name']} - {entry['Score']} - {entry['Date']}" #formats leaderboard text

            label = font.render(text, True, (255, 255, 255)) #renders leaderboard text in white
            x = screen_rect.centerx - label.get_width() // 2 #horizontal position of text (centered)
            screenL.blit(label, (x, y_offset)) #positions leaderboard text
            y_offset += 60 #increments y position for next entry

        if back_button.draw(screenL): #back button to main menu
            click.play()
            current_state = "main_menu"
            pygame.time.delay(200) #delay to prevent multiple clicks
            return(current_state)
        
            
        
        return "leaderboard_screen"
