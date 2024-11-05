import pygame
import sys
import asyncio
import time

from colors import *
from food import FoodController
from utils import show_info, check
from wall import WallController
from snake import Snake, SnakeBodyBlock

# set window size and name
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# initial speed
INITIAL_SNAKE_SPEED = 10
INITIAL_SNAKE_COLOR = WHITE

# max food cnt, max wall cnt
MAX_FOOD_CNT = 3
MAX_WALL_CNT = 1

GENERATE_WALL_INTERVAL = 10  # seconds

WINDOW_CAPTION = "UserName-蛇吃豆-UserID"


# game over function
async def game_over(screen, code: int, score: int):
    """game over function

    Args:
        code (int): 0: collision with the wall, 1: collision with the snake body, 2: collision with the wall
    """
    if code == 0:
        print("Game Over because of collision with the wall")
    elif code == 1:
        print("Game Over because of collision with the snake body")
    elif code == 2:
        print("Game Over because of collision with the wall")

    my_font = pygame.font.SysFont("times new roman", 50)
    game_over_surface = my_font.render("Your Score is : " + str(score), True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    await asyncio.sleep(4)
    pygame.quit()
    sys.exit()


async def main():
    # initialize the pygame
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_CAPTION)

    # init snake direction
    snake_direction = "RIGHT"
    change_to = snake_direction
    new_snake_direction = snake_direction

    # initial score
    score = 0

    # Function to display hints
    def show_hints(screen):
        font = pygame.font.SysFont("times new roman", 20)
        hints = [
            "Use arrow keys or WASD to move the snake.",
            "Press SPACE to restart the game.",
        ]
        for i, hint in enumerate(hints):
            hint_surface = font.render(hint, True, WHITE)
            hint_rect = hint_surface.get_rect(topleft=(10, 10 + i * 25))
            screen.blit(hint_surface, hint_rect)

    snake = Snake(
        body=[
            SnakeBodyBlock(
                pos=(390, 390),
                color=INITIAL_SNAKE_COLOR,
                width=10,
                height=10,
            ),
            SnakeBodyBlock(
                pos=(400, 390),
                color=INITIAL_SNAKE_COLOR,
                width=10,
                height=10,
            ),
        ],
        direction="RIGHT",
    )

    # generate food and wall
    food_controller = FoodController(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
    )
    food_controller.generate(MAX_FOOD_CNT, snake.get_all_pos())

    wall_controller = WallController(
        walls=None, width=SCREEN_WIDTH, height=SCREEN_HEIGHT
    )
    wall_controller.generate(
        MAX_WALL_CNT, food_controller.get_pos(), snake.get_all_pos()
    )

    # init time and tick settings
    start_time = time.time()
    fps = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, ord("w"), ord("W"), ord("k"), ord("K")]:
                    change_to = "UP"
                elif event.key in [
                    pygame.K_DOWN,
                    ord("s"),
                    ord("S"),
                    ord("j"),
                    ord("J"),
                ]:
                    change_to = "DOWN"
                elif event.key in [
                    pygame.K_LEFT,
                    ord("a"),
                    ord("A"),
                    ord("h"),
                    ord("H"),
                ]:
                    change_to = "LEFT"
                elif event.key in [
                    pygame.K_RIGHT,
                    ord("d"),
                    ord("D"),
                    ord("l"),
                    ord("L"),
                ]:
                    change_to = "RIGHT"

        current_snake_direction = snake.get_direction()
        # Handle direction changes
        if change_to == "UP" and current_snake_direction != "DOWN":
            new_snake_direction = "UP"
        if change_to == "DOWN" and current_snake_direction != "UP":
            new_snake_direction = "DOWN"
        if change_to == "LEFT" and current_snake_direction != "RIGHT":
            new_snake_direction = "LEFT"
        if change_to == "RIGHT" and current_snake_direction != "LEFT":
            new_snake_direction = "RIGHT"

        snake.set_direction(new_snake_direction)

        food_pos = food_controller.get_pos(idx="all")
        snake_head_pos = snake.get_head_pos()

        is_food_eaten = check(food_pos, snake_head_pos)
        if is_food_eaten:
            eaten_food_idx = food_controller.get_food_at_pos(pos=snake_head_pos)
            eaten_food = food_controller.get_food(idx=eaten_food_idx)

            score += eaten_food.get_score()
            snake.grow(color=eaten_food.color)

            food_controller.remove(idx=eaten_food_idx)
            food_controller.generate(
                1, snake.get_all_pos(), wall_controller.get_all_collision()
            )
        else:
            snake.move()

        # Draw everything
        screen.fill(BLACK)
        food_controller.draw(screen=screen)
        wall_controller.draw(screen=screen)
        snake.draw(screen=screen)

        # Show hints
        show_hints(screen)

        # Game Over conditions
        snake_head_pos = snake.get_head_pos()
        if snake_head_pos[0] < 0 or snake_head_pos[0] > SCREEN_WIDTH - 10:
            await game_over(screen, 0, score)
        if snake_head_pos[1] < 0 or snake_head_pos[1] > SCREEN_HEIGHT - 10:
            await game_over(screen, 0, score)

        # Touching the snake body
        if check(snake_head_pos, [block.pos for block in snake.body[-2::-1]]):
            await game_over(screen, 1, score)

        if check(snake_head_pos, wall_controller.get_all_collision()):
            await game_over(screen, 2, score)

        show_info(
            screen=screen,
            place="upperright",
            score=score,
            time_played=(time.time() - start_time),
        )

        # Refresh game screen
        pygame.display.flip()

        # generate a new wall per GENERATE_WALL_INTERVAL
        if (
            time.time() - start_time
        ) / GENERATE_WALL_INTERVAL > wall_controller.count():
            wall_controller.generate(1, food_controller.get_pos(), snake.get_all_pos())

        # Frame Per Second /Refresh Rate
        snake_speed = INITIAL_SNAKE_SPEED + 2 / 60 * max(
            0, (time.time() - start_time - 1)
        )
        fps.tick(snake_speed)

        # Required for web environment
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
