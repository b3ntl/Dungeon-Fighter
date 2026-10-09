import pygame, os

class Animation:
    
    #animation constructor (folder with animations, time displayed, option to resize images)
    def __init__(self, folder_path, frame_time=120, scale = None):
        
        self.frames = []    #list to store frames
        self.index = 0      #frame number
        self.frame_time = frame_time    #time frame displayed for
        self.last_update = pygame.time.get_ticks()  #time since last frame to know when to advance
        
        for file in sorted (os.listdir(folder_path)):   #loops through files/frames in sorted order
            image = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()  #os.p.j creates full path

            #changes scale
            if scale:
                image = pygame.transform.scale(image, scale)
            
            #appends frame images to the list    
            self.frames.append(image)
    
    #updates animation frames        
    def update(self):
        
        now = pygame.time.get_ticks()   #gets current time
        
        if now - self.last_update >= self.frame_time:   #checks if enough time has passed to advance
            self.index = (self.index +1) %  len(self.frames)    #moves to next frame, %len loops back to frame 0 after last frame
            self.last_update = now  #resets timer to change frame
    
    #returns to 1st frame        
    def reset(self):
        self.index = 0
    
    #returns current frame    
    def get_image(self):
        return self.frames[self.index]