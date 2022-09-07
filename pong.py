import pygame
import random

# initialize all pygame modules (font, display, etc.)
pygame.init()

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 950

class Paddle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def draw_window(surface):
    pass

def main(surface):
    pass

def main_menu(window):
    pass

# initialize window and open main menu
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption("Pong")
main_menu(window)