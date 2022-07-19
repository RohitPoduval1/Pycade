import pygame  # Main game module
from pygame.math import Vector2  # Used for positions
from sys import exit
from os.path import dirname, join  # For taking images from the "Assets" folder


colors = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "BROWN": (125, 48, 17),
}

pygame.init()

FPS = 60

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400

directory_name = dirname(__file__)

pygame.display.set_caption("CS50P Final Project: Archery 🏹")

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.font.init()
TEXT_SIZE = 50
TEXT_COLOR = (0, 255, 0)
text_font = pygame.font.SysFont("Comic Sans MS", TEXT_SIZE)


class Player:

    BOW_IMAGE = pygame.image.load(join(directory_name, "Assets", "bow.png")).convert_alpha()
    WIDTH, HEIGHT = 57, 63
    MOVEMENT_SPEED = 3.4

    def __init__(self):
        self.pos = Vector2(
            WINDOW_WIDTH/2 - Player.WIDTH/2,
            WINDOW_HEIGHT - Player.HEIGHT
        )

    def move(self, direction):  # TODO: Test
        if direction.lower() == "left":
            self.pos.x -= Player.MOVEMENT_SPEED
        elif direction.lower() == "right":
            self.pos.x += Player.MOVEMENT_SPEED
        else:
            raise ValueError("Invalid direction")

    def reset(self, level):
        if level == 2:
            self.pos = Vector2(274.5, WINDOW_HEIGHT - Player.HEIGHT)
        else:
            self.pos = Vector2(
                WINDOW_WIDTH/2 - Player.WIDTH/2,
                WINDOW_HEIGHT - Player.HEIGHT
            )

    def has_reached_left_edge(self):  # TODO: Test
        return self.pos.x < Player.MOVEMENT_SPEED

    def has_reached_right_edge(self):
        return self.pos.x > WINDOW_WIDTH - Player.WIDTH - Player.MOVEMENT_SPEED

    def draw(self):
        WINDOW.blit(
            Player.BOW_IMAGE,
            pygame.Rect(self.pos.x, self.pos.y, Player.WIDTH, Player.HEIGHT),
        )


class Arrow:

    ARROW_IMAGE = pygame.image.load(join(directory_name, "Assets", "arrow.png")).convert_alpha()
    WIDTH, HEIGHT = 5, 10
    MOVEMENT_SPEED = 3.4

    def __init__(self, player_x_pos):  # TODO: Test initializing with valid/invalid player x pos
        if player_x_pos > WINDOW_WIDTH or player_x_pos < 0:
            raise ValueError("Invalid player x position")
        else:
            self.pos = Vector2(
                player_x_pos + Player.WIDTH/2,
                WINDOW_HEIGHT - Player.HEIGHT
            )
        self.is_shot = False
        self.rect = pygame.Rect(
            self.pos.x,
            self.pos.y - Arrow.HEIGHT,
            Arrow.WIDTH,
            Arrow.HEIGHT
        )

    def _reset(self):
        self.is_shot = False
        self.pos.y = WINDOW_HEIGHT - Player.HEIGHT

    def update_pos(self, player_x_pos, has_collided_with_arrow):
        if self.is_shot:
            self.pos.y -= Arrow.MOVEMENT_SPEED
        self.pos.x = player_x_pos + Player.WIDTH/2  # keeps the arrow following the player's x-position
        if has_collided_with_arrow:
            self._reset()

    def draw(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, Arrow.WIDTH, Arrow.HEIGHT)
        if self.pos.y > 0:  # if the arrow is still onscreen
            WINDOW.blit(    # keep drawing the arrow
                Arrow.ARROW_IMAGE,
                pygame.Rect(self.pos.x, self.pos.y, Arrow.WIDTH, Arrow.HEIGHT),
            )
        else:               # else, the arrow is offscreen
            self._reset()   # so reset it


class Target:

    TARGET = pygame.image.load(join(directory_name, "Assets", "target.png")).convert_alpha()
    WIDTH, HEIGHT = 30, 30

    def __init__(self, x_pos, y_pos):
        self.pos = Vector2(x_pos, y_pos)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, Target.WIDTH, Target.HEIGHT)
        self._has_been_hit = False

    def has_collided_with_arrow(self, arrow_rect):  # TODO: Possible test by importing pygame and making Rects
        self._has_been_hit = pygame.Rect.colliderect(self.rect, arrow_rect)
        return pygame.Rect.colliderect(self.rect, arrow_rect)

    def draw(self):
        if not self._has_been_hit:
            self.rect = pygame.Rect(self.pos.x, self.pos.y, self.WIDTH, self.HEIGHT)
            WINDOW.blit(self.TARGET, self.rect)


class Obstacle:

    game_over = False

    def __init__(self, width, height, x_pos, y_pos):
        self.pos = Vector2(x_pos, y_pos)
        self.WIDTH, self.HEIGHT = width, height
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.WIDTH, self.HEIGHT)
        self.color = colors["RED"]

    def has_collided_with_arrow(self, arrow_rect):
        return pygame.Rect.colliderect(self.rect, arrow_rect)

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)


class Main:

    BACKGROUND_COLOR = colors["BLACK"]

    def __init__(self):
        self.player = Player()

        self.arrow = Arrow(player_x_pos=self.player.pos.x)

        # LEVEL 1 (Face 😐)
        # Target for level 1 (Placed like a 👃)
        self.target_1 = Target(
            x_pos=((WINDOW_WIDTH / 3) + ((2 / 3) * WINDOW_WIDTH)) / 2 - 10, y_pos=160
        )
        self.obstacle_1_eye_1 = Obstacle(
            width=15,
            height=(1 / 4) * (WINDOW_WIDTH / 3),
            x_pos=(1 / 3) * WINDOW_WIDTH,
            y_pos=WINDOW_HEIGHT / 3 - 50
        )
        self.obstacle_1_eye_2 = Obstacle(
            width=15,
            height=(1 / 4) * (WINDOW_WIDTH / 3),
            x_pos=(2 / 3) * WINDOW_WIDTH,
            y_pos=WINDOW_HEIGHT / 3 - 50
        )
        self.obstacle_1_mouth = Obstacle(
            width=140,
            height=15,
            x_pos=WINDOW_WIDTH / 2 - 60,
            y_pos=WINDOW_HEIGHT / 3 * 2,
        )

        # LEVEL 2
        # Target for level 2
        self.target_2 = Target(x_pos=274.5, y_pos=50)
        # Obstacles for level 2
        self.obstacle_2_1 = Obstacle(
            width=(2 / 3) * (WINDOW_WIDTH / 3),
            height=15,
            x_pos=WINDOW_WIDTH / 3,
            y_pos=WINDOW_HEIGHT - Player.HEIGHT * 1.5 - 35,
        )
        self.obstacle_2_2 = Obstacle(
            width=self.obstacle_2_1.WIDTH - 5,
            height=self.obstacle_2_1.HEIGHT,
            x_pos=WINDOW_WIDTH - (WINDOW_WIDTH / 3) - Player.WIDTH - Player.MOVEMENT_SPEED - ((2 / 3) * (WINDOW_WIDTH / 3)) / 2,
            y_pos=WINDOW_HEIGHT / 4,
        )

        # LEVEL 3
        # Target for level 3
        self.target_3 = Target(
            x_pos=WINDOW_WIDTH / 2 - self.target_1.WIDTH * 4,
            y_pos=5
        )
        # Obstacles for level 3
        self.obstacle_3_1 = Obstacle(  # Bottom gateway (Left)
            width=60,
            height=66,
            x_pos=0,
            y_pos=WINDOW_HEIGHT - 150
        )
        self.obstacle_3_2 = Obstacle(  # Bottom gateway (Right)
            width=WINDOW_WIDTH - self.obstacle_3_1.WIDTH - 20,
            height=self.obstacle_3_1.HEIGHT,
            x_pos=77,
            y_pos=self.obstacle_3_1.pos.y,
        )
        self.obstacle_3_3 = Obstacle(  # Top gateway (Right)
            width=487,
            height=self.obstacle_3_1.HEIGHT,
            x_pos=113,
            y_pos=110
        )
        self.obstacle_3_4 = Obstacle(  # Top gateway (Left)
            width=100,
            height=self.obstacle_3_1.HEIGHT,
            x_pos=0,
            y_pos=self.obstacle_3_3.pos.y,
        )

        # LEVEL 4
        # Obstacles for level 4
        self.obstacle_4_C_1 = Obstacle(width=100, height=12, x_pos=30, y_pos=50)
        self.obstacle_4_C_2 = Obstacle(
            width=self.obstacle_4_C_1.HEIGHT,
            height=120,
            x_pos=self.obstacle_4_C_1.pos.x,
            y_pos=self.obstacle_4_C_1.pos.y,
        )
        self.obstacle_4_C_3 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=self.obstacle_4_C_1.pos.x,
            y_pos=self.obstacle_4_C_1.pos.y + self.obstacle_4_C_1.WIDTH + (1.5 * self.obstacle_4_C_1.HEIGHT),
        )

        self.obstacle_4_S_1 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=150,
            y_pos=self.obstacle_4_C_1.pos.y,
        )
        self.obstacle_4_S_2 = Obstacle(
            width=self.obstacle_4_C_2.WIDTH,
            height=self.obstacle_4_C_2.HEIGHT / 2,
            x_pos=self.obstacle_4_S_1.pos.x,
            y_pos=self.obstacle_4_S_1.pos.y,
        )
        self.obstacle_4_S_3 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=self.obstacle_4_S_1.pos.x,
            y_pos=(self.obstacle_4_C_3.pos.y + self.obstacle_4_C_1.pos.y) / 2,
        )
        self.obstacle_4_S_4 = Obstacle(
            width=self.obstacle_4_S_2.WIDTH,
            height=self.obstacle_4_S_2.HEIGHT,
            x_pos=self.obstacle_4_S_1.pos.x + self.obstacle_4_S_1.WIDTH - self.obstacle_4_C_1.HEIGHT,
            y_pos=(self.obstacle_4_C_3.pos.y + self.obstacle_4_C_1.pos.y) / 2,
        )
        self.obstacle_4_S_5 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=self.obstacle_4_S_1.pos.x,
            y_pos=self.obstacle_4_C_3.pos.y,
        )

        self.obstacle_4_five_1 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=340,
            y_pos=self.obstacle_4_C_1.pos.y,
        )
        self.obstacle_4_five_2 = Obstacle(
            width=self.obstacle_4_C_2.WIDTH,
            height=self.obstacle_4_C_2.HEIGHT / 2,
            x_pos=self.obstacle_4_five_1.pos.x,
            y_pos=self.obstacle_4_five_1.pos.y,
        )
        self.obstacle_4_five_3 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=self.obstacle_4_five_1.pos.x,
            y_pos=(self.obstacle_4_C_3.pos.y + self.obstacle_4_C_1.pos.y) / 2,
        )
        self.obstacle_4_five_4 = Obstacle(
            width=self.obstacle_4_S_2.WIDTH,
            height=self.obstacle_4_S_2.HEIGHT,
            x_pos=self.obstacle_4_five_1.pos.x + self.obstacle_4_five_1.WIDTH - self.obstacle_4_S_2.WIDTH,
            y_pos=(self.obstacle_4_C_3.pos.y + self.obstacle_4_C_1.pos.y) / 2,
        )
        self.obstacle_4_five_5 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=self.obstacle_4_five_1.pos.x,
            y_pos=self.obstacle_4_C_3.pos.y,
        )

        self.obstacle_4_zero_1 = Obstacle(
            width=self.obstacle_4_C_1.WIDTH,
            height=self.obstacle_4_C_1.HEIGHT,
            x_pos=460,
            y_pos=self.obstacle_4_C_1.pos.y,
        )
        self.obstacle_4_zero_2 = Obstacle(
            width=self.obstacle_4_C_2.WIDTH,
            height=self.obstacle_4_C_2.HEIGHT,
            x_pos=self.obstacle_4_zero_1.pos.x + self.obstacle_4_zero_1.WIDTH - self.obstacle_4_zero_1.HEIGHT,
            y_pos=self.obstacle_4_C_1.pos.y,
        )
        self.obstacle_4_zero_3 = Obstacle(
            width=self.obstacle_4_C_2.WIDTH,
            height=self.obstacle_4_C_2.HEIGHT,
            x_pos=self.obstacle_4_zero_1.pos.x,
            y_pos=self.obstacle_4_zero_1.pos.y,
        )
        self.obstacle_4_zero_4 = Obstacle(
            width=self.obstacle_4_zero_1.WIDTH,
            height=self.obstacle_4_zero_1.HEIGHT,
            x_pos=self.obstacle_4_zero_1.pos.x,
            y_pos=self.obstacle_4_zero_1.pos.y + self.obstacle_4_zero_2.HEIGHT,
        )
        # Target for level 4
        self.target_4 = Target(
            x_pos=(self.obstacle_4_C_1.pos.x + self.obstacle_4_C_1.WIDTH) / 2 + 130,
            y_pos=(self.obstacle_4_C_2.pos.y + self.obstacle_4_C_2.HEIGHT) / 2 - 20,
        )

        self.level = 1

    def draw_window(self):
        if not Obstacle.game_over:

            self.draw_background()

            # Face 😐
            if self.level == 1:
                self.player.draw()
                self.obstacle_1_eye_1.draw()
                self.obstacle_1_eye_2.draw()
                self.obstacle_1_mouth.draw()
                self.target_1.draw()
                if self.target_1.has_collided_with_arrow(self.arrow.rect):
                    self.draw_win_screen()
                    self.level += 1
                    self.player.reset(self.level)

            # Narrow Passage
            elif self.level == 2:
                self.player.draw()

                # The walls do not function as obstacles in the sense the the player is able to collide with them and still continue, so rectangles will suffice
                # Left Wall
                pygame.draw.rect(
                    WINDOW,
                    colors["BROWN"],
                    pygame.Rect(
                        0,
                        0,
                        WINDOW_WIDTH / 3,
                        WINDOW_HEIGHT
                    )
                )
                # Right Wall
                pygame.draw.rect(
                    WINDOW,
                    colors["BROWN"],
                    pygame.Rect(
                        WINDOW_WIDTH - (WINDOW_WIDTH / 3),
                        0,
                        WINDOW_WIDTH / 3,
                        WINDOW_HEIGHT,
                    )
                )
                self.obstacle_2_1.draw()
                self.obstacle_2_2.draw()
                self.target_2.draw()
                if self.target_2.has_collided_with_arrow(self.arrow.rect):
                    self.draw_win_screen()
                    self.level += 1
                    self.player.reset(self.level)

            # Gateways
            elif self.level == 3:
                self.player.draw()
                self.obstacle_3_1.draw()
                self.obstacle_3_2.draw()
                self.obstacle_3_3.draw()
                self.obstacle_3_4.draw()
                self.target_3.draw()
                if self.target_3.has_collided_with_arrow(self.arrow.rect):
                    self.draw_win_screen()
                    self.level += 1
                    self.player.reset(self.level)

            # CS50
            elif self.level == 4:
                self.player.draw()
                # C
                self.obstacle_4_C_1.draw()
                self.obstacle_4_C_2.draw()
                self.obstacle_4_C_3.draw()
                # S
                self.obstacle_4_S_1.draw()
                self.obstacle_4_S_2.draw()
                self.obstacle_4_S_3.draw()
                self.obstacle_4_S_4.draw()
                self.obstacle_4_S_5.draw()
                # 5
                self.obstacle_4_five_1.draw()
                self.obstacle_4_five_2.draw()
                self.obstacle_4_five_3.draw()
                self.obstacle_4_five_4.draw()
                self.obstacle_4_five_5.draw()
                # 0
                self.obstacle_4_zero_1.draw()
                self.obstacle_4_zero_2.draw()
                self.obstacle_4_zero_3.draw()
                self.obstacle_4_zero_4.draw()
                # Target
                self.target_4.draw()

            # If the arrow is shot during an active game, draw it no matter what
            if self.arrow.is_shot:
                self.arrow.draw()

            if self.target_4.has_collided_with_arrow(self.arrow.rect):
                self.draw_win_screen()

        else:
            self.draw_background()
            self.draw_game_over_screen()
        pygame.display.update()

    def draw_background(self):
        pygame.draw.rect(
            WINDOW,
            Main.BACKGROUND_COLOR,
            pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def draw_win_screen(self):
        pygame.draw.rect(
            WINDOW,
            Main.BACKGROUND_COLOR,
            pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        WINDOW.blit(
            text_font.render("YOU WIN!", False, TEXT_COLOR),
            (WINDOW_WIDTH / 2 - TEXT_SIZE*2.5, WINDOW_HEIGHT/2 - TEXT_SIZE)
        )
        pygame.time.wait(1300)

    def draw_game_over_screen(self):
        WINDOW.blit(
            text_font.render("GAME OVER :(", False, TEXT_COLOR),
            (WINDOW_WIDTH/4, WINDOW_HEIGHT/3)
        )


main_game = Main()


def main():

    player_pressed_left, player_pressed_right = False, False

    clock = pygame.time.Clock()

    running = True
    while running:

        clock.tick(FPS)

        if main_game.level == 1:
            main_game.arrow.update_pos(
                main_game.player.pos.x,
                main_game.target_1.has_collided_with_arrow(main_game.arrow.rect)
            )
            Obstacle.game_over = (
                main_game.obstacle_1_mouth.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_1_eye_1.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_1_eye_2.has_collided_with_arrow(main_game.arrow.rect)
            )

        elif main_game.level == 2:
            main_game.arrow.update_pos(
                main_game.player.pos.x,
                main_game.target_2.has_collided_with_arrow(main_game.arrow.rect)
            )
            Obstacle.game_over = (
                main_game.obstacle_2_1.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_2_2.has_collided_with_arrow(main_game.arrow.rect)
            )

        elif main_game.level == 3:
            main_game.arrow.update_pos(
                main_game.player.pos.x,
                main_game.target_3.has_collided_with_arrow(main_game.arrow.rect)
            )
            Obstacle.game_over = (
                main_game.obstacle_3_1.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_3_2.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_3_3.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_3_4.has_collided_with_arrow(main_game.arrow.rect)
            )

        elif main_game.level == 4:
            main_game.arrow.update_pos(
                main_game.player.pos.x,
                main_game.target_4.has_collided_with_arrow(main_game.arrow.rect)
            )
            Obstacle.game_over = (
                main_game.obstacle_4_C_1.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_C_2.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_C_3.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_S_1.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_S_2.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_S_3.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_S_4.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_S_5.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_five_1.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_five_2.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_five_3.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_five_4.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_five_5.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_zero_1.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_zero_2.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_zero_3.has_collided_with_arrow(main_game.arrow.rect)
                or main_game.obstacle_4_zero_4.has_collided_with_arrow(main_game.arrow.rect)
            )

        for event in pygame.event.get():

            # User closed the window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            # Check for key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_pressed_left = True
                elif event.key == pygame.K_RIGHT:
                    player_pressed_right = True

                elif event.key == pygame.K_SPACE:
                    main_game.arrow.is_shot = True

                elif event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    exit()

            # Check for key releases
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_pressed_left = False
                elif event.key == pygame.K_RIGHT:
                    player_pressed_right = False

        # Handler for holding down keys for movement
        if player_pressed_left:
            if main_game.level == 2:
                if (not main_game.player.pos.x < WINDOW_WIDTH/3 + Player.MOVEMENT_SPEED):
                    main_game.player.move("LEFT")
            else:
                if (not main_game.player.has_reached_left_edge()):  # Prevents player from going off the screen
                    main_game.player.move("LEFT")

        elif player_pressed_right:
            if main_game.level == 2:
                if (not main_game.player.pos.x > WINDOW_WIDTH - (WINDOW_WIDTH / 3) - Player.WIDTH - Player.MOVEMENT_SPEED):
                    main_game.player.move("RIGHT")
            else:
                if (not main_game.player.has_reached_right_edge()):  # Prevents player from going off the screen
                    main_game.player.move("RIGHT")

        main_game.draw_window()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
