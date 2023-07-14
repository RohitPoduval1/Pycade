from random import randint
import pygame  # Main game module
from pygame.math import Vector2  # Used for positions
from sys import exit
from os.path import dirname, join  # For taking images from the "Assets" folder


# TODO: Add a csv for high scores
# TODO: Add sprites
# (taxi credit to pch.vector on freepik.com)

colors = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BROWN": (125, 48, 17)
}

pygame.init()

FPS = 60

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 350

directory_name = dirname(__file__)

pygame.display.set_caption("Traffic")

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Player:
    
    WIDTH, HEIGHT = 30, 30

    def __init__(self):
        self.pos = Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT-75)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, Player.WIDTH, Player.HEIGHT) 
        self.lane = 1

    # Updates the x position of the player depending on which lane they are in
    def _lane_handler(self):
        if self.lane == 1:  # Middle 
            self.pos.x = WINDOW_WIDTH / 2
        elif self.lane == 0:  # Left
            self.pos.x = WINDOW_WIDTH / 7
        elif self.lane == 2:  # Right
            self.pos.x = WINDOW_WIDTH - WINDOW_WIDTH/7 - Player.WIDTH
        else:
            raise ValueError("Invalid lane position")
        self.rect = pygame.Rect(self.pos.x, self.pos.y, Player.WIDTH, Player.HEIGHT) 

    # Draws the player on 1 of 3 lanes
    def draw(self):
        self._lane_handler()
        return pygame.draw.rect(WINDOW, colors["GREEN"], self.rect)


class Obstacle:
    
    MOVEMENT_SPEED = 2

    def __init__(self):
        self.lane, self.prev_lane = randint(0, 2), 3
        if self.lane == 1:  # Middle 
            self.pos = Vector2(WINDOW_WIDTH / 2, 0)
        elif self.lane == 0:  # Left
            self.pos = Vector2(WINDOW_WIDTH / 7, 0)
        elif self.lane == 2:  # Right
            self.pos = Vector2(WINDOW_WIDTH - WINDOW_WIDTH/7 - Player.WIDTH, 0)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, Player.WIDTH, Player.HEIGHT) 
    
    def _lane_handler(self):
        if self.lane == 1:  # Middle 
            self.pos.x = WINDOW_WIDTH / 2
        elif self.lane == 0:  # Left
            self.pos.x = WINDOW_WIDTH / 7
        elif self.lane == 2:  # Right
            self.pos.x = WINDOW_WIDTH - WINDOW_WIDTH/7 - Player.WIDTH
        else:
            raise ValueError(f"Invalid lane position{self.lane}")

    def collided_with_player(self, player_pos):
        return pygame.Rect.colliderect(
            self.rect,
            pygame.Rect(player_pos.x, player_pos.y, Player.WIDTH, Player.HEIGHT)
        )

    def draw(self):
        self._lane_handler()
        self.pos.y += Obstacle.MOVEMENT_SPEED
        self.rect = pygame.Rect(self.pos.x, self.pos.y, Player.WIDTH, Player.HEIGHT)
        return pygame.draw.rect(WINDOW, colors["RED"], self.rect)


class Main:

    def __init__(self):
        self.player = Player()
        self.obstacle1 = Obstacle()
        self.obstacle2 = Obstacle()
        self.score = 0

    def _get_different_random_num(self, prev, min, max):
        new_num = randint(min, max)
        if new_num == prev:
            return self._get_different_random_num(prev, min, max)
        else:
            return new_num

    # def play_music(self):
    #     pygame.mixer.init()
    #     pygame.mixer.music.load(self.MUSIC)
    #     pygame.mixer.music.play(loops=-1)  # Infinite loop

    def _draw_background(self):
        pygame.draw.rect(WINDOW, colors["BLACK"], pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def _draw_score(self):
        pygame.font.init()
        _score_font = pygame.font.SysFont("Comic Sans MS", round(WINDOW_HEIGHT / 10))

        # displaying the scores
        WINDOW.blit(
            _score_font.render(str(self.score), False, colors["WHITE"]),
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2),
        )
        
    def draw_window(self):
        self._draw_background()
        self._draw_score()
        self.player.draw()
        if self.obstacle1.pos.y < WINDOW_HEIGHT or self.obstacle2.pos.y < WINDOW_HEIGHT:
            self.obstacle1.draw()
            self.obstacle2.draw()
        else:
            self.obstacle1.prev_lane = self.obstacle1.lane
            self.obstacle1.lane = self._get_different_random_num(self.obstacle1.prev_lane, 0, 2)
            self.obstacle1.pos.y = 0

            self.obstacle2.prev_lane = self.obstacle2.lane
            self.obstacle2.lane = self._get_different_random_num(self.obstacle2.prev_lane, 0, 2)
            self.obstacle2.pos.y = 0

            Obstacle.MOVEMENT_SPEED += .3
            self.score += 1

        pygame.display.update()

UPDATE = pygame.USEREVENT
UPDATE_TIMER = 1
pygame.time.set_timer(UPDATE, UPDATE_TIMER) 

main_game = Main()
def main():

    clock = pygame.time.Clock()

    running = True
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            # User closed the window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            
            # elif event.type == UPDATE:
            #     main_game.obstacle1.is_offscreen = main_game.obstacle1.pos.y > WINDOW_HEIGHT

            # Check for key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if 0 < main_game.player.lane <= 2:
                        main_game.player.lane -= 1
                elif event.key == pygame.K_RIGHT:
                    if 0 <= main_game.player.lane <= 1:
                        main_game.player.lane += 1

                elif event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    exit()

        # Game Over logic
        if (main_game.obstacle1.collided_with_player(main_game.player.pos) or main_game.obstacle2.collided_with_player(main_game.player.pos)):
            running = False
            pygame.quit()
            exit()

        main_game.draw_window()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
