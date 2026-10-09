import pygame, health, volume_screen

#sounds
pygame.mixer.init()
heal = pygame.mixer.Sound('Sounds/heal.mp3')
shield = pygame.mixer.Sound('Sounds/shield.mp3')
armour = pygame.mixer.Sound('Sounds/armour.mp3')

#heal.set_volume(volume_screen.music_volume)
#shield.set_volume(volume_screen.music_volume)
#armour.set_volume(volume_screen.music_volume)



#item class
class Item:
    def __init__(self, name, image_path, effect):
        self.name = name    #item name
        self.image = pygame.image.load(image_path).convert_alpha()  #item image location
        self.rect = self.image.get_rect()   #image
        self.effect = effect  # function called when item is used

    #draw item on screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)


#item functions/effects

#heal player (health potion)
def heal_player(player):
    heal.play()
    health.health_bar.health = min(
        health.health_bar.max_health,
        health.health_bar.health + 30 #add 30 health
    )

#shield
def give_shield(player):
    shield.play()
    player.start_invincibility(8000, (0, 100, 255)) #temporary shield
                            #8 seconds, colour

#armour                            
def restore_armour(player):
    armour.play()
    health.restore_armour_full()

#item creation

def create_health_potion(x, y):
    item = Item(
        "Health Potion",
        "Images/healthpotion.png",
        heal_player #heal player function
    )
    item.rect.center = (x, y)
    return item

def create_shield(x, y):
    item = Item(
        "Shield",
        "Images/shield.png",
        give_shield #give shield function
    )
    item.rect.center = (x, y)   #item position
    return item

def create_armour(x, y):
    item = Item("Armour",
                "Images/armour.png",
                restore_armour)
    item.rect.center = (x, y)
    return item