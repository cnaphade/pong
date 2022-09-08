import pygame
import random

# initialize all pygame modules (font, display, etc.)
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PLAY_WIDTH = SCREEN_WIDTH * 0.9
PLAY_HEIGHT = SCREEN_HEIGHT * 0.9
WINDOW_COLOR = (10, 15, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# top-left xy coordinates (origin frame of reference)
top_left_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2
top_left_y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

class Paddle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def draw_window(surface):
    surface.fill(WINDOW_COLOR)

    # draw play area
    pygame.draw.rect(surface, BLACK, (top_left_x, top_left_y, PLAY_WIDTH, PLAY_HEIGHT), 0)
    
    # draw center line
    midpoints = []
    midpoint_x = top_left_x + (PLAY_WIDTH // 2)
    line_width = PLAY_HEIGHT // 80
    for midpoint_y in range(int(top_left_y), int(top_left_y + PLAY_HEIGHT)):
        if midpoint_y % line_width == 0:
            midpoints.append((midpoint_x, midpoint_y))
    for i in range(1, len(midpoints), 2):
        pygame.draw.lines(surface, WHITE, False, [midpoints[i], midpoints[i - 1]], 2)

def main(surface, single):
    global SCREEN_WIDTH, SCREEN_HEIGHT, PLAY_WIDTH, PLAY_HEIGHT, top_left_x, top_left_y
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                PLAY_WIDTH = SCREEN_WIDTH * 0.9
                PLAY_HEIGHT = SCREEN_HEIGHT * 0.9
                top_left_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2
                top_left_y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

                old_surface = surface
                surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                surface.blit(old_surface, (0, 0))
                del old_surface
            
            if event.type == pygame.KEYDOWN:
                continue
        
        # render play
        draw_window(surface)
        pygame.display.update()

def main_menu(window):
    global SCREEN_WIDTH, SCREEN_HEIGHT

    run = True
    while run:
        window.fill(WINDOW_COLOR)
        # Title
        title_size = SCREEN_HEIGHT // 5
        font = pygame.font.SysFont('couriernew', title_size, bold = True)
        title = font.render('pong', 1, WHITE)
        title_x = (SCREEN_WIDTH - title.get_width()) / 2
        title_y = (SCREEN_HEIGHT - title.get_height()) / 2
        window.blit(title, (title_x, title_y))

        # Play Against Computer
        label_size = SCREEN_HEIGHT // 40
        font = pygame.font.SysFont('futura', label_size)
        label = font.render('Press 1 to play against Computer', 1, WHITE)
        label_x = (SCREEN_WIDTH - label.get_width()) / 2
        label_y = title_y + (title.get_height() * 1.5)
        window.blit(label, (label_x, label_y))

        # Play Against Another Person
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