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

    # initialize a new gamestate object
    def initialize(self, config):
        self.config = config
        self.sound_config = SoundConfig()
        self.paddle_1 = Paddle(x = self.config.PLAY_WIDTH - ((self.config.PLAY_WIDTH / 100) * 3), 
                        y = (self.config.PLAY_HEIGHT - (self.config.PLAY_HEIGHT / 12)) / 2, 
                        width = self.config.PLAY_WIDTH / 100, height = self.config.PLAY_HEIGHT / 12, score = 0)
        self.paddle_2 = Paddle(x = (self.config.PLAY_WIDTH / 100) * 2, 
                        y = (self.config.PLAY_HEIGHT - (self.config.PLAY_HEIGHT / 12)) / 2, 
                        width = self.config.PLAY_WIDTH / 100, height = self.config.PLAY_HEIGHT / 12, score = 0)
        self.ball = Ball(x = self.config.PLAY_WIDTH / 2, y = self.config.PLAY_HEIGHT / 2, size = 10, 
                    speed_x = 3, speed_y = 0, direction_x = 1, direction_y = 0)

    # reset paddle dimensions and location
    def reset_paddles(self):
        self.paddle_1.width = self.config.PLAY_WIDTH / 100
        self.paddle_1.height = self.config.PLAY_HEIGHT / 12
        self.paddle_2.width = self.paddle_1.width
        self.paddle_2.height = self.paddle_1.height

        self.paddle_1.x = self.config.PLAY_WIDTH - (self.paddle_1.width * 3)
        self.paddle_1.y = (self.config.PLAY_HEIGHT - self.paddle_1.height) / 2
        self.paddle_2.x = self.paddle_2.width * 2
        self.paddle_2.y = (self.config.PLAY_HEIGHT - self.paddle_2.height) / 2

    # set ball speed and direction upon paddle hit
    def paddle_hit_rebound(self, paddle, direction):
        self.ball.direction_x = direction

        if self.ball.speed_x < 5:
                self.ball.speed_x += 1
        # set y speed and direction of ball based on what part of the paddle it hits
        if self.ball.y + self.ball.size <= paddle.y + (paddle.height * 2 / 5):
            self.ball.direction_y = -1
            if self.ball.speed_y < 5:
                self.ball.speed_y += 1.5
        elif self.ball.y >= paddle.y + (paddle.height * 3 / 5):
            self.ball.direction_y = 1
            if self.ball.speed_y < 5:
                self.ball.speed_y += 1.5
        else:
            self.ball.direction_y = random.choice([-0.5, 0, 0.5])
            self.ball.speed_y = random.choice([-1, 0, 1])

    # move physics simulation forward by dt
    def time_progression(self, dt, impulse, computer_play):
        # move paddle_1 up-impulse:0 down-impulse:1
        if self.paddle_1.y - impulse[0] >= self.paddle_1.width:
            self.paddle_1.y -= impulse[0]
        if self.paddle_1.y + self.paddle_1.height + impulse[1] <= config.PLAY_HEIGHT - self.paddle_1.width:
            self.paddle_1.y += impulse[1]
        # move paddle_2 up-impulse:2 down-impulse:3
        if self.paddle_2.y - impulse[2] >= self.paddle_2.width:
            self.paddle_2.y -= impulse[2]
        if self.paddle_2.y + self.paddle_2.height + impulse[3] <= config.PLAY_HEIGHT - self.paddle_2.width:
            self.paddle_2.y += impulse[3]
        
        # computer play
        if computer_play:
            if self.ball.x < config.PLAY_WIDTH / 2:
                # move computer down
                if self.paddle_2.y + self.paddle_2.height < self.ball.y:
                    if self.paddle_2.y + self.paddle_2.height + 4 <= config.PLAY_HEIGHT - self.paddle_2.width:
                        self.paddle_2.y += 4
                # move computer up
                elif self.paddle_2.y > self.ball.y and self.paddle_2.y - 4 >= self.paddle_2.width:
                    self.paddle_2.y -= 4
            # move computer to center
            elif self.paddle_2.y <= (config.PLAY_HEIGHT - self.paddle_2.height) / 2:
                self.paddle_2.y += 1
            elif self.paddle_2.y > (config.PLAY_HEIGHT - self.paddle_2.height) / 2:
                self.paddle_2.y -= 1

        # move ball
        self.ball.x += self.ball.speed_x * self.ball.direction_x * dt
        self.ball.y += self.ball.speed_y * self.ball.direction_y * dt

        # handle collision of ball with paddles and boundaries
        # check paddle_1 hit
        if self.ball.x + self.ball.size >= self.paddle_1.x:
            if self.ball.y + self.ball.size >= self.paddle_1.y:
                if self.ball.y <= self.paddle_1.y + self.paddle_1.height:
                    self.paddle_hit_rebound(self.paddle_1, -1)
                    return self.sound_config.paddle_hit_sound
            
        # check paddle_2 hit
        if self.ball.x <= self.paddle_2.x + self.paddle_2.width:
            if self.ball.y + self.ball.size >= self.paddle_2.y:
                if self.ball.y <= self.paddle_2.y + self.paddle_2.height:
                    self.paddle_hit_rebound(self.paddle_2, 1)
                    return self.sound_config.paddle_hit_sound

        # check upper and lower boundary hit
        if self.ball.y <= 0 or self.ball.y + self.ball.size >= self.config.PLAY_HEIGHT:
            self.ball.direction_y *= -1      
            return self.sound_config.boundary_hit_sound

        # check if ball crosses player boundary and count score
        point_scored = False
        if self.ball.x + self.ball.size < self.paddle_2.x:
            self.paddle_1.score += 1
            self.ball.direction_x = -1
            point_scored = True
        elif self.ball.x > self.paddle_1.x + self.paddle_1.width:
            self.paddle_2.score += 1
            self.ball.direction_x = 1
            point_scored = True

        # reset ball position after scores
        if point_scored:
            self.ball.x = self.config.PLAY_WIDTH / 2
            self.ball.y = self.config.PLAY_HEIGHT / 2
            self.ball.speed_x = 2
            self.ball.speed_y = 0
            self.ball.direction_y = 0
            return self.sound_config.score_sound

def play_sound(sound):
    pygame.mixer.Sound.play(sound)

def main(surface, config, multiplayer):
    run = True
    game_state = GameState()
    game_state.initialize(config)

    paddle_1 = game_state.paddle_1
    paddle_2 = game_state.paddle_2
    ball = game_state.ball
    pygame.key.set_repeat(2)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.VIDEORESIZE:
                config.reset_config(event.w, event.h)
                game_state.reset_paddles()

        # player controls
        keys = pygame.key.get_pressed()
        impulse = [0 for _ in range(4)]
        # move player 1 up
        if keys[pygame.K_UP]:
            impulse[0] = 4
        # move player_1 down
        if keys[pygame.K_DOWN]:
            impulse[1] = 4
        
        # human player_2 play
        if multiplayer:
            # move player 2 up
            if keys[pygame.K_w]:
                impulse[2] = 4
            # move player 2 down
            if keys[pygame.K_s]:
                impulse[3] = 4
            
        # move game forward by one timestep
        interaction = game_state.time_progression(1, impulse, not multiplayer)
        if interaction:
            play_sound(interaction)

        # render play
        draw_play_window(surface, game_state, config)
        display_score(surface, game_state, config)
        
        if check_victory(surface, game_state, config):
            run = False

def main_menu(window, config):
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
config = Config()
window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
main_menu(window, config)