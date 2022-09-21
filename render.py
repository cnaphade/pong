import pygame

WINDOW_COLOR = (10, 15, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_main_menu(window, config):
    window.fill(WINDOW_COLOR)
    # Title
    title_size = config.SCREEN_HEIGHT // 5
    font = pygame.font.SysFont('couriernew', title_size, bold = True)
    title = font.render('pong', 1, WHITE)
    title_x = (config.SCREEN_WIDTH - title.get_width()) / 2
    title_y = (config.SCREEN_HEIGHT - title.get_height()) / 2
    window.blit(title, (title_x, title_y))

    # Play Against Computer
    label_size = config.SCREEN_HEIGHT // 40
    font = pygame.font.SysFont('futura', label_size)
    label = font.render('Press 1 to play against Computer', 1, WHITE)
    label_x = (config.SCREEN_WIDTH - label.get_width()) / 2
    label_y = title_y + (title.get_height() * 1.5)
    window.blit(label, (label_x, label_y))

    # Play Against Another Person
    label_size = config.SCREEN_HEIGHT // 40
    font = pygame.font.SysFont('futura', label_size)
    label = font.render('Press 2 to play Multiplayer', 1, WHITE)
    label_x = (config.SCREEN_WIDTH - label.get_width()) / 2
    label_y = label_y + (label.get_height() * 1.5)
    window.blit(label, (label_x, label_y))
    pygame.display.update()

# klauria: make a submodule called render.py and put all rendering code there. Expose only the single rendering function that takes State and Config.
def draw_play_window(surface, state, config):
    # top-left xy coordinates (origin frame of reference)
    top_left_x = (config.SCREEN_WIDTH - config.PLAY_WIDTH) / 2
    top_left_y = (config.SCREEN_HEIGHT - config.PLAY_HEIGHT) / 2

    surface.fill(WINDOW_COLOR)

    # draw play area
    pygame.draw.rect(surface, BLACK, (top_left_x, top_left_y, config.PLAY_WIDTH, config.PLAY_HEIGHT), 0)
    
    # draw center line
    midpoints = []
    midpoint_x = top_left_x + (config.PLAY_WIDTH // 2)
    line_width = config.PLAY_HEIGHT // 80
    for midpoint_y in range(int(top_left_y), int(top_left_y + config.PLAY_HEIGHT)):
        if midpoint_y % line_width == 0:
            midpoints.append((midpoint_x, midpoint_y))
    for i in range(1, len(midpoints), 2):
        pygame.draw.lines(surface, WHITE, False, [midpoints[i], midpoints[i - 1]], 2)
    
    # draw paddles
    pygame.draw.rect(surface, WHITE, (top_left_x + state.paddle_1.x, top_left_y + state.paddle_1.y, state.paddle_1.width, state.paddle_1.height), 0)
    pygame.draw.rect(surface, WHITE, (top_left_x + state.paddle_2.x, top_left_y + state.paddle_2.y, state.paddle_2.width, state.paddle_2.height), 0)

    # draw ball
    pygame.draw.rect(surface, WHITE, (top_left_x + state.ball.x, top_left_y + state.ball.y, state.ball.size, state.ball.size))

# show player scores at the top
def display_score(surface, state, config):
    # top-left xy coordinates (origin frame of reference)
    top_left_x = (config.SCREEN_WIDTH - config.PLAY_WIDTH) / 2
    top_left_y = (config.SCREEN_HEIGHT - config.PLAY_HEIGHT) / 2

    # show player_1 score
    label_size = config.SCREEN_HEIGHT // 20
    font = pygame.font.SysFont('futura', label_size)
    label = font.render(str(state.paddle_1.score), 1, WHITE)
    label_x = top_left_x + (config.PLAY_WIDTH // 2) + label.get_width()
    label_y = top_left_y + label.get_height()
    surface.blit(label, (label_x, label_y))
    
    # show player_2 score
    label_size = config.SCREEN_HEIGHT // 20
    font = pygame.font.SysFont('futura', label_size)
    label = font.render(str(state.paddle_2.score), 1, WHITE)
    label_x = top_left_x + (config.PLAY_WIDTH // 2) - (label.get_width() * 2)
    label_y = top_left_y + label.get_height()
    surface.blit(label, (label_x, label_y))
    pygame.display.update()

def check_victory(surface, state, config):
    # top-left xy coordinates (origin frame of reference)
    top_left_x = (config.SCREEN_WIDTH - config.PLAY_WIDTH) / 2
    top_left_y = (config.SCREEN_HEIGHT - config.PLAY_HEIGHT) / 2

    victory = False
    if state.paddle_1.score == 10:
        # player-1 win message
        player_side = top_left_x + (config.PLAY_WIDTH * 3 / 4)
        victory = True
    elif state.paddle_2.score == 10:
        # player-2 win message
        player_side = top_left_x + (config.PLAY_WIDTH * 1 / 4)
        victory = True

    if victory:
        label_size = config.SCREEN_HEIGHT // 20
        font = pygame.font.SysFont('futura', label_size)
        label = font.render('WINNER', 1, WHITE)
        label_x = player_side - (label.get_width() // 2)
        label_y = top_left_y + (config.PLAY_HEIGHT // 2) - (label.get_height() // 2)
        surface.blit(label, (label_x, label_y))
        pygame.display.update()
        pygame.time.delay(4000)

    return victory