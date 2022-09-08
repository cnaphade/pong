import pygame
import random

# initialize all pygame modules (font, display, etc.)
pygame.init()

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 950
WHITE = (255, 255, 255)

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

def main(surface, single):
    pass

def main_menu(window):
    global SCREEN_WIDTH, SCREEN_HEIGHT

    run = True
    while run:
        window.fill((0, 0, 0))
        # Title
        title_size = SCREEN_HEIGHT // 5
        font = pygame.font.SysFont('couriernew', title_size, bold = True)
        title = font.render('pong', 1, WHITE)
        title_x = (SCREEN_WIDTH - title.get_width()) / 2
        title_y = (SCREEN_HEIGHT - title.get_height()) / 2
        window.blit(title, (title_x, title_y))

        # Play Mode
        label_size = SCREEN_HEIGHT // 40
        font = pygame.font.SysFont('futura', label_size)
        label = font.render('Press 1 to play against Computer', 1, WHITE)
        label_x = (SCREEN_WIDTH - label.get_width()) / 2
        label_y = title_y + (title.get_height() * 1.5)
        window.blit(label, (label_x, label_y))

        label_size = SCREEN_HEIGHT // 40
        font = pygame.font.SysFont('futura', label_size)
        label = font.render('Press 2 to play Multiplayer', 1, WHITE)
        label_x = (SCREEN_WIDTH - label.get_width()) / 2
        label_y = label_y + (label.get_height() * 1.5)
        window.blit(label, (label_x, label_y))
        pygame.display.update()

        # start or quit game (allow resize too)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main(window, single = True)
                if event.key == pygame.K_2:
                    main(window, single = False)
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                old_window = window
                window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                window.blit(old_window, (0, 0))
                del old_window

    pygame.display.quit()

# initialize window and open main menu
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
main_menu(window)