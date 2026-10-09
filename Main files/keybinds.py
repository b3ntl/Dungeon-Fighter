
import pygame

keybinds = {
    "move_up": pygame.K_w,
    "move_down": pygame.K_s,
    "move_left": pygame.K_a,
    "move_right": pygame.K_d,
    "attack": pygame.K_SPACE,
    "mouse_attack": 1  # left click
}

def set_wasd():
    keybinds["move_up"] = pygame.K_w
    keybinds["move_down"] = pygame.K_s
    keybinds["move_left"] = pygame.K_a
    keybinds["move_right"] = pygame.K_d

def set_arrows():
    keybinds["move_up"] = pygame.K_UP
    keybinds["move_down"] = pygame.K_DOWN
    keybinds["move_left"] = pygame.K_LEFT
    keybinds["move_right"] = pygame.K_RIGHT

def set_attack_space():
    keybinds["attack"] = pygame.K_SPACE

def set_attack_mouse():
    keybinds["attack"] = "mouse"
