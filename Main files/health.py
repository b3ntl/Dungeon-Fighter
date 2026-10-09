import pygame

screen_width = 1200
screen_height = 750

#health bar setup--------------------------------------------------------------------------------------------------------------------------------
class player_health_bar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = max_health #initial health value set as max health
        self.max_health = max_health #store max health for scaling the health bar

    def draw_health(self, screenGame):
        ratio = self.health / self.max_health #calculate health ratio for scaling the health bar
        pygame.draw.rect(screenGame, "red", (self.x, self.y, self.width, self.height)) #draw background of health bar (red)
        pygame.draw.rect(screenGame, "green", (self.x, self.y, self.width * ratio, self.height)) #draw foreground of health bar (green) scaled by health ratio
     
class player_shield_bar:
    def __init__ (self, x, y, width, height, max_shield):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shield = 0 #start at 0
        self.shield = max_shield
        self.max_shield = 50
        
    def draw_shield (self, screenGame):
        ratio = self.shield / self.max_shield
        pygame.draw.rect(screenGame, (60,60,60), (self.x, self.y, self.width, self.height)) # dark grey background
        pygame.draw.rect(screenGame, (0, 150, 255), (self.x, self.y, self.width * ratio, self.height)) # blue shield bar
        
x = screen_width - 300 -20   # 20px padding from the edge (300 = width)
y = 40                       # 40px from the top

shield_x = x - 150 - 20
shield_y = 40
        
health_bar = player_health_bar(x, y, 300, 30, 100) #x, y, width, height, max health
shield_bar = player_shield_bar(shield_x, shield_y, 150, 30, 50)

def apply_damage (amount: int):
    if amount <=0:
        return
    
    #armour first
    if shield_bar.shield > 0:
        absorbed = min(amount, shield_bar.shield)
        shield_bar.shield -= absorbed
        amount -= absorbed
    
    #leftover damage to health
    if amount >0:
        health_bar.health = max (0, health_bar.health - amount)
        
def restore_armour_full():
    shield_bar.shield = shield_bar.max_shield