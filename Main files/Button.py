import pygame

#button class
class button(): #creates class
    def __init__(self, x, y, image, scale): #creates constructor
        width = image.get_width() #gets image width
        height = image.get_height() #gets image height
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()   #creates rectangle with the image
        self.rect.topleft = (x, y)   #creates coordinate for top left of image
        self.clicked = False
        
    def draw(self, surface):
        action = False
        #mouseposition
        pos = pygame.mouse.get_pos() #gets position
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:   #0 is lmk, checks whether lm has clicked on the rectangle
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:   #if mouse isn't clicking button
                self.clicked = False    #sets back to false
                
        #draw button
        surface.blit(self.image, (self.rect.x, self.rect.y)) #draws the button

        return action
    
class slider(): #slider class
            def __init__ (self, pos: tuple, size: tuple, initial_val: float, min: int, max: int, handle_width: int) -> None: #constructor method
                self.pos = pos #position of slider centre variable
                self.size = size #size variable
                self.handle_width = int(handle_width) #handle width variable
                
                self.slider_left_pos = self.pos[0] - (size[0]/2) #left position of slider       #remove half the width from centre x pos
                self.slider_right_pos = self.pos[0] + (size[0]/2) #right position of slider     #add half the width to centre x pos
                self.slider_top_pos = self.pos[1] - (size[1]/2) #top position of slider         #remove half the height from centre y pos
                
                self.min = min #minimum value variable
                self.max = max #maximum value variable
                self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val #initial value variable #as percentage of slider length (easier to calculate)
                
                self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, size[0], size[1]) #container rectangle
                self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - self.handle_width/2, self.slider_top_pos, self.handle_width, self.size[1]) #button rectangle
            
            def move_slider(self, mouse_pos):
                x = max(self.slider_left_pos, min(self.slider_right_pos, mouse_pos[0]))  #clamp mouse x position within slider bounds
                self.button_rect.centerx = x  #sets button centre x to clamped mouse x position
                self.button_rect.centery = self.container_rect.centery  #sets button centre y to slider centre y (prevents vertical movement)
            
            def render (self,surface):  #render method for debugging
                pygame.draw.rect(surface, "darkgrey", self.container_rect)  #draw container
                pygame.draw.rect(surface, "red", self.button_rect)   #draw button

            def getValue(self):   #get value method
                val_range = self.slider_right_pos - self.slider_left_pos - 1  #value range variable
                button_val = self.button_rect.centerx - self.slider_left_pos  #button value variable
                
                return (button_val / val_range) * (self.max - self.min) + self.min  #returns value as per min and max
                        #gets percentage of button position in slider and scales to min and max