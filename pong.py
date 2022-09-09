import pygame
import random

# initialize all pygame modules (font, display, etc.)
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PLAY_WIDTH = SCREEN_WIDTH * 0.9
PLAY_HEIGHT = SCREEN_HEIGHT * 0.9
PADDLE_WIDTH = PLAY_WIDTH // 100
PADDLE_HEIGHT = PLAY_HEIGHT // 8
BALL_SIZE = 10
WINDOW_COLOR = (10, 15, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# top-left xy coordinates (origin frame of reference)
top_left_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2
top_left_y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

class Paddle(object):
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score

class Ball(object):
    def __init__(self, x, y, speed, direction_x, direction_y):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction_x = direction_x
        self.direction_y = direction_y

def draw_window(surface, paddle_1, paddle_2, ball):
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
    
    # draw paddles
    pygame.draw.rect(surface, WHITE, (paddle_1.x, paddle_1.y, PADDLE_WIDTH, PADDLE_HEIGHT), 0)
    pygame.draw.rect(surface, WHITE, (paddle_2.x, paddle_2.y, PADDLE_WIDTH, PADDLE_HEIGHT), 0)

    # draw ball
    pygame.draw.rect(surface, WHITE, (ball.x, ball.y, BALL_SIZE, BALL_SIZE))

# set ball speed and direction upon paddle hit
def paddle_hit_rebound(paddle, ball):
    ball.direction_x *= -1
    if ball.speed < 8:
            ball.speed += 1
    # set y-direction of ball based on what part of the paddle it hits
    if ball.y + BALL_SIZE <= paddle.y + (PADDLE_HEIGHT * 2 / 5):
        ball.direction_y = -1
    elif ball.y >= paddle.y + (PADDLE_HEIGHT * 3 / 5):
        ball.direction_y = 1
    else:
        ball.direction_y = 0

# handle collision of ball with paddles and boundaries
def collision(paddle_1, paddle_2, ball):
    # check paddle_1 hit
    if ball.x >= paddle_1.x and ball.y + BALL_SIZE >= paddle_1.y and ball.y <= paddle_1.y + PADDLE_HEIGHT:
        paddle_hit_rebound(paddle_1, ball)
        
    # check paddle_2 hit
    if ball.x <= paddle_2.x + PADDLE_WIDTH and ball.y + BALL_SIZE >= paddle_2.y and ball.y <= paddle_2.y + PADDLE_HEIGHT:
        paddle_hit_rebound(paddle_2, ball)

    # check boundary hit
    if ball.y <= top_left_y or ball.y + BALL_SIZE >= top_left_y + PLAY_HEIGHT:
        ball.direction_y *= -1

# check if ball crosses player boundary and count score
def point_scored(paddle_1, paddle_2, ball):
    if ball.x + BALL_SIZE < paddle_2.x:
        paddle_1.score += 1
        ball.direction_x = -1
        return True
    elif ball.x > paddle_1.x + PADDLE_WIDTH:
        paddle_2.score += 1
        ball.direction_x = 1
        return True

    return False

def main(surface, multiplayer):
    global SCREEN_WIDTH, SCREEN_HEIGHT, PLAY_WIDTH, PLAY_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, top_left_x, top_left_y
    
    run = True
    player_1 = Paddle(top_left_x + PLAY_WIDTH - (PADDLE_WIDTH * 3), top_left_y + (PLAY_HEIGHT // 2), 0)
    player_2 = Paddle(top_left_x + (PADDLE_WIDTH * 2), top_left_y + (PLAY_HEIGHT // 2), 0)
    ball = Ball(top_left_x + (PLAY_WIDTH // 2), top_left_y + (PLAY_HEIGHT // 2), 4, 1, 0)

    pygame.key.set_repeat(2)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                PLAY_WIDTH = SCREEN_WIDTH * 0.9
                PLAY_HEIGHT = SCREEN_HEIGHT * 0.9
                PADDLE_WIDTH = PLAY_WIDTH // 100
                PADDLE_HEIGHT = PLAY_HEIGHT // 8
                top_left_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2
                top_left_y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

                player_1.x = top_left_x + PLAY_WIDTH - (PADDLE_WIDTH * 3)
                player_1.y = top_left_y + (PLAY_HEIGHT // 2)
                player_2.x = top_left_x + (PADDLE_WIDTH * 2)
                player_2.y = top_left_y + (PLAY_HEIGHT // 2)

                old_surface = surface
                surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                surface.blit(old_surface, (0, 0))
                del old_surface
            
        keys = pygame.key.get_pressed()
        # move player_1 down
        if keys[pygame.K_DOWN]:
            if player_1.y + PADDLE_HEIGHT + 4 <= top_left_y + PLAY_HEIGHT - PADDLE_WIDTH:
                player_1.y += 4
        # move player 1 up
        if keys[pygame.K_UP]:
            if player_1.y - 4 >= top_left_y + PADDLE_WIDTH:
                player_1.y -= 4
        # move player 2 down
        if multiplayer and keys[pygame.K_s]:
            if player_2.y + PADDLE_HEIGHT + 4 <= top_left_y + PLAY_HEIGHT - PADDLE_WIDTH:
                player_2.y += 4
        # move player 2 up
        if multiplayer and keys[pygame.K_w]:
            if player_2.y - 4 >= top_left_y + PADDLE_WIDTH:
                player_2.y -= 4
        
        if not multiplayer:
            if ball.x < top_left_x + (PLAY_WIDTH / 2):
                # move computer down
                if player_2.y + (PADDLE_HEIGHT / 2) < ball.y and player_2.y + PADDLE_HEIGHT + 2.75 <= top_left_y + PLAY_HEIGHT - PADDLE_WIDTH:
                    player_2.y += 2.75
                # move computer up
                elif player_2.y + (PADDLE_HEIGHT / 2) > ball.y and player_2.y - 2.75 >= top_left_y + PADDLE_WIDTH:
                    player_2.y -= 2.75
            # move computer to center
            elif player_2.y <= (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2:
                player_2.y += 2
            elif player_2.y > (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2:
                player_2.y -= 2
        
        # handle ball collisions with wall and paddles
        collision(player_1, player_2, ball)     
        
        # reset ball position after scores
        if point_scored(player_1, player_2, ball):
            ball.x = top_left_x + (PLAY_WIDTH // 2)
            ball.y = top_left_y + (PLAY_HEIGHT // 2)
            ball.speed = 4
            ball.direction_y = 0

        # move ball
        ball.x += (ball.speed / 2) * ball.direction_x
        ball.y += (ball.speed / 2) * ball.direction_y
        
        # render play
        draw_window(surface, player_1, player_2, ball)
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
                    main(window, multiplayer = False)
                if event.key == pygame.K_2:
                    main(window, multiplayer = True)
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