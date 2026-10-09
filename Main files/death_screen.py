import pygame, Button, json, os
from datetime import datetime

pygame.init()
screen_width = 1200
screen_height = 750
screenD = pygame.display.set_mode((screen_width, screen_height)) #creates display screen

pygame.mixer.init()
click = pygame.mixer.Sound('Sounds/click.mp3')

background = pygame.Surface((screen_width, screen_height)) #create background surface
background.fill((0, 0, 0)) #fill background with black

font = pygame.font.SysFont("Arial", 50, bold=True)
font_small = pygame.font.SysFont("Arial", 30, bold=True)

#button & Images
enter_img = pygame.image.load('Images/enter.png').convert_alpha()
enter_button = Button.button(screen_width // 2 - enter_img.get_width() // 2, screen_height - 100, enter_img, 3) #enter button object

enter_button.rect.centerx = screenD.get_rect().centerx #center enter button horizontally
enter_button.rect.bottom = screenD.get_rect().bottom - 200 #position enter button 50 pixels from bottom of screen

#max length of initials
max_length = 3

def save_score(initials, score):
            data = [] #initialize empty list for leaderboard data
            if os.path.exists("leaderboard.json"):
                with open("leaderboard.json", "r") as file:
                    try:
                        data = json.load(file) #load existing leaderboard data
                    except json.JSONDecodeError:
                        data = [] #if file is empty or invalid, start with empty list
                        
            #append new score to data list
            new_entry = {"Name": initials, "Score": score, "Date": datetime.now().strftime("%d/%m/%Y")} #create new leaderboard entry with initials, score, and current date
            data.append(new_entry)
            data.sort(key=lambda x: x["Score"], reverse=True) #sort leaderboard data by score in descending order
            data = data[:10] #keep only top 10 scores
            
            #save updated leaderboard data back to file
            with open("leaderboard.json", "w") as file:
                json.dump(data, file, indent=4) #write updated data to file with indentation for readability
            
def Drun(final_score):
    initials = "" #initialize empty string for player initials
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            
            elif event.type == pygame.KEYDOWN:
                
                #allow backspace to delete characters
                if event.key == pygame.K_BACKSPACE: #allow backspace to delete characters
                    initials = initials[:-1]
                
                #only allow letter inputs for initials, and limit length to max_length
                elif pygame.K_a <= event.key <= pygame.K_z:
                    if len(initials) < max_length: #only allow input if initials are less than max length
                        initials += chr(event.key).upper() #add uppercase character to initials string based on key pressed
                
                #enter key submits initials and saves score        
                elif event.key == pygame.K_RETURN: #submit initials on enter key
                    if len(initials) > 0: #only submit if at least one character has been entered
                        click.play()
                        save_score(initials, final_score) #save score with player initials
                        return "leaderboard_screen" #go to leaderboard screen after submitting score
            
        #draw death screen
        screenD.fill((0, 0, 0)) #clear screen with black background
        
        #title text
        label = font.render("You Died!", True, (255, 0, 0)) #red text for title
        screenD.blit(label, (600 - label.get_width() // 2, 120)) #center title text horizontally and position vertically at 120px from top
        
        #final score text
        score_text = font_small.render(f"Final Score: {final_score}", True, (255, 255, 255)) #white text for final score
        screenD.blit(score_text, (600 - score_text.get_width() // 2, 250)) #center score text horizontally and position vertically below title
        
        #Enter initials prompt
        prompt_text = font_small.render("Enter your initials:", True, (255, 255, 255)) #white text for initials prompt
        screenD.blit(prompt_text, (600 - prompt_text.get_width() // 2, 300)) #center prompt text horizontally and position vertically below score
        
        #initials input display
        initials_label = font.render(initials, True, (255, 255, 255)) #white text for initials input
        screenD.blit(initials_label, (600 - initials_label.get_width() // 2, 350)) #center initials input horizontally and position vertically below score
        
        #draw enter button
        if enter_button.draw(screenD):
            if len(initials) > 0: #only submit if at least one character has been entered
                click.play()
                save_score(initials, final_score) #save score with player initials
                return "leaderboard_screen" #go to leaderboard screen after submitting score
        
        pygame.display.update() #update display each frame