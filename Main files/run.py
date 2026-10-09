import pygame, Button, settings_screen, leaderboard_screen, volume_screen, keybinds_screen
import main_menu, sys, game, death_screen

current_state = "main_menu"

#game loop
run = True
previous_state = None
while run: #checks for whether the game has been exited
    
    state_before = current_state
    
    if current_state == "main_menu":
        result = main_menu.Mrun()
        current_state = result
        
    elif current_state == "settings_screen":
        result = settings_screen.Srun()
        current_state = result
        
    elif current_state == "volume_screen":
        result = volume_screen.Vrun()
        current_state = result
    
    elif current_state == "keybinds_screen":
        result = keybinds_screen.Krun()
        current_state = result
        
    elif current_state == "leaderboard_screen":
        result = leaderboard_screen.Lrun()
        current_state = result
        
    elif current_state == "game":
        if previous_state in ["main_menu"]:
            game.reset_game()
        result = game.gameRun()
        current_score = game.score #get current score from game module
        current_state = result
                    
    elif current_state == "death_screen":
        result = death_screen.Drun(final_score=current_score) #call death screen function and store result
        current_state = result
    
    if result == "exit":
        run = False
        break
    
    if result is not None: #if result is not None, it means a state change has occurred, so update the current state
        current_state = result
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
            
    #update previous state
    previous_state = state_before
                        
    pygame.display.update() #updates the game window

pygame.quit() #quits the game once the while loop has ended