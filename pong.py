# klauria: as discussed, make a State object that contains the ball and paddles, and has a function to step the physics simulation forward by the given dt.
# klauria: also as discussed, make a function to render the game state to the screen. Nothing else should know about the screen width and height, or anything to do with pixels.
# klauria: please read about dataclasses in Python, and rewrite Paddle and Object to be dataclasses.
import pygame
import random
from dataclasses import dataclass
from render import *

# initialize all pygame modules (font, display, etc.)
pygame.init()

# klauria: put these in a class called Config. Make it a dataclass. No globals please!
@dataclass
class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    PLAY_WIDTH = SCREEN_WIDTH * 0.9
    PLAY_HEIGHT = SCREEN_HEIGHT * 0.9

    def reset_config(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.PLAY_WIDTH = self.SCREEN_WIDTH * 0.9
        self.PLAY_HEIGHT = self.SCREEN_HEIGHT * 0.9

# klauria: Put these in a dataclass called SoundConfig.
# game sounds
@dataclass
class SoundConfig:
    paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
    boundary_hit_sound = pygame.mixer.Sound("boundary_hit.wav")
    score_sound = pygame.mixer.Sound("score.wav")

# Paddle class
@dataclass
class Paddle:
    x: float
    y: float
    width: float
    height: float
    score: int

# Ball class
@dataclass
class Ball:
    x: float
    y: float
    size: float
    speed_x: float
    speed_y: float
    direction_x: int
    direction_y: int

@dataclass
class GameState:
    config: Config = None
    paddle_1: Paddle = None
    paddle_2: Paddle = None
    ball: Ball = None

    def initialize(self, config):
        self.config = config
        self.paddle_1 = Paddle(x = self.config.PLAY_WIDTH - ((self.config.PLAY_WIDTH / 100) * 3), 
                        y = (self.config.PLAY_HEIGHT - (self.config.PLAY_HEIGHT / 10)) / 2, 
                        width = self.config.PLAY_WIDTH / 100, height = self.config.PLAY_HEIGHT / 8, score = 0)
        self.paddle_2 = Paddle(x = (self.config.PLAY_WIDTH / 100) * 2, 
                        y = (self.config.PLAY_HEIGHT - (self.config.PLAY_HEIGHT / 10)) / 2, 
                        width = self.config.PLAY_WIDTH / 100, height = self.config.PLAY_HEIGHT / 8, score = 0)
        self.ball = Ball(x = self.config.PLAY_WIDTH / 2, y = self.config.PLAY_HEIGHT / 2, size = 10, 
                    speed_x = 3, speed_y = 0, direction_x = 1, direction_y = 0)

    def reset_paddles(self):
        self.paddle_1.width = self.config.PLAY_WIDTH / 100
        self.paddle_1.height = self.config.PLAY_HEIGHT / 10
        self.paddle_2.width = self.paddle_1.width
        self.paddle_2.height = self.paddle_1.height

        self.paddle_1.x = self.config.PLAY_WIDTH - (self.paddle_1.width * 3)
        self.paddle_1.y = (self.config.PLAY_HEIGHT - self.paddle_1.height) / 2
        self.paddle_2.x = self.paddle_2.width * 2
        self.paddle_2.y = (self.config.PLAY_HEIGHT - self.paddle_2.height) / 2

    def time_progression(self, dt):
        # move ball
        self.ball.x += self.ball.speed_x * self.ball.direction_x * dt
        self.ball.y += self.ball.speed_y * self.ball.direction_y * dt      
    
    def play_sound(self, sound):
        pygame.mixer.Sound.play(sound)
        
# set ball speed and direction upon paddle hit
def paddle_hit_rebound(paddle, ball, direction):
    ball.direction_x = direction

    if ball.speed_x < 5:
            ball.speed_x += 1
    # set y speed and direction of ball based on what part of the paddle it hits
    if ball.y + ball.size <= paddle.y + (paddle.height * 2 / 5):
        ball.direction_y = -1
        if ball.speed_y < 5:
            ball.speed_y += 1.5
    elif ball.y >= paddle.y + (paddle.height * 3 / 5):
        ball.direction_y = 1
        if ball.speed_y < 5:
            ball.speed_y += 1.5
    else:
        ball.direction_y = random.choice([-0.5, 0, 0.5])
        ball.speed_y = random.choice([-1, 0, 1])

# handle collision of ball with paddles and boundaries
def collision(game_state, config, sound_config):
    paddle_1 = game_state.paddle_1
    paddle_2 = game_state.paddle_2
    ball = game_state.ball

    # check paddle_1 hit
    if ball.x + ball.size >= paddle_1.x:
        if ball.y + ball.size >= paddle_1.y:
            if ball.y <= paddle_1.y + paddle_1.height:
                game_state.play_sound(sound_config.paddle_hit_sound)
                paddle_hit_rebound(paddle_1, ball, -1)
        
    # check paddle_2 hit
    if ball.x <= paddle_2.x + paddle_2.width:
        if ball.y + ball.size >= paddle_2.y:
            if ball.y <= paddle_2.y + paddle_2.height:
                game_state.play_sound(sound_config.paddle_hit_sound)
                paddle_hit_rebound(paddle_2, ball, 1)

    # check upper and lower boundary hit
    if ball.y <= 0 or ball.y + ball.size >= config.PLAY_HEIGHT:
        game_state.play_sound(sound_config.boundary_hit_sound)
        ball.direction_y *= -1

# check if ball crosses player boundary and count score
def point_scored(game_state):
    if game_state.ball.x + game_state.ball.size < game_state.paddle_2.x:
        game_state.paddle_1.score += 1
        game_state.ball.direction_x = -1
        return True
    elif game_state.ball.x > game_state.paddle_1.x + game_state.paddle_1.width:
        game_state.paddle_2.score += 1
        game_state.ball.direction_x = 1
        return True
    return False

def main(surface, config, multiplayer):
    run = True
    sound_config = SoundConfig()
    game_state = GameState()
    game_state.initialize(config)

    paddle_1 = game_state.paddle_1
    paddle_2 = game_state.paddle_2
    ball = game_state.ball
    pygame.key.set_repeat(2)

    while run:
        # move game forward by one timestep
        game_state.time_progression(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.VIDEORESIZE:
                config.reset_config(event.w, event.h)
                game_state.reset_paddles()

        # player controls
        keys = pygame.key.get_pressed()
        # move player_1 down
        if keys[pygame.K_DOWN]:
            if paddle_1.y + paddle_1.height + 4 <= config.PLAY_HEIGHT - paddle_1.width:
                paddle_1.y += 4
        # move player 1 up
        if keys[pygame.K_UP]:
            if paddle_1.y - 4 >= paddle_1.width:
                paddle_1.y -= 4
        
        # human player_2 play
        if multiplayer:
            # move player 2 down
            if keys[pygame.K_s]:
                if paddle_2.y + paddle_2.height + 4 <= config.PLAY_HEIGHT - paddle_2.width:
                    paddle_2.y += 4
            # move player 2 up
            if keys[pygame.K_w]:
                if paddle_2.y - 4 >= paddle_2.width:
                    paddle_2.y -= 4
        
        # computer play
        if not multiplayer:
            if ball.x < config.PLAY_WIDTH / 2:
                # move computer down
                if paddle_2.y + paddle_2.height < ball.y:
                    if paddle_2.y + paddle_2.height + 4 <= config.PLAY_HEIGHT - paddle_2.width:
                        paddle_2.y += 4
                # move computer up
                elif paddle_2.y > ball.y and paddle_2.y - 4 >= paddle_2.width:
                    paddle_2.y -= 4
            # move computer to center
            elif paddle_2.y <= (config.PLAY_HEIGHT - paddle_2.height) / 2:
                paddle_2.y += 1
            elif paddle_2.y > (config.PLAY_HEIGHT - paddle_2.height) / 2:
                paddle_2.y -= 1

        # handle ball collisions with wall and paddles
        collision(game_state, config, sound_config)     
        
        # reset ball position after scores
        if point_scored(game_state):
            game_state.play_sound(sound_config.score_sound)
            ball.x = config.PLAY_WIDTH / 2
            ball.y = config.PLAY_HEIGHT / 2
            ball.speed_x = 2
            ball.speed_y = 0
            ball.direction_y = 0
        
        # render play
        draw_play_window(surface, game_state, config)
        display_score(surface, game_state, config)
        
        if check_victory(surface, game_state, config):
            run = False

def main_menu(window):
    config = Config()
    run = True
    while run:
        draw_main_menu(window, config)
        # start or quit game (allow resize too)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main(window, config, multiplayer = False)
                if event.key == pygame.K_2:
                    main(window, config, multiplayer = True)
            if event.type == pygame.VIDEORESIZE:
                config.reset_config(event.w, event.h)

    pygame.display.quit()

# initialize window and open main menu
window = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
main_menu(window)