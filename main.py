import pygame
import sys
import time

from base_class import Block
from colors import *
from food import FoodController
from utils import *
from wall import WallController
from snake import Snake, SnakeBodyBlock

# set window size and name
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# initial speed
INITIAL_SNAKE_SPEED = 10
INITIAL_SNAKE_COLOR = WHITE

# max fooc cnt, max wall cnt
MAX_FOOD_CNT = 3
MAX_WALL_CNT = 1

GENERATE_WALL_INTERVAL = 10  # seconds

WINDOW_CAPTION = "USerName-蛇吃豆-UserID"

# init snake direction
INIT_SNAKE_DIRECTION = "RIGHT"
snake_direction = INIT_SNAKE_DIRECTION
change_to = snake_direction

# initial score
score = 0

# initialize the pygame
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_CAPTION)

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
    direction=INIT_SNAKE_DIRECTION,
)

# generate food and wall
food_controller = FoodController(
    width=SCREEN_WIDTH,
    height=SCREEN_HEIGHT,
)
food_controller.generate(MAX_FOOD_CNT, snake.get_all_pos())

wall_controller = WallController(walls=None, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
wall_controller.generate(MAX_WALL_CNT, food_controller.get_pos(), snake.get_all_pos())


# game over function
def game_over(code: int):
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
    else:
        pass
    # creating font object my_font
    my_font = pygame.font.SysFont("times new roman", 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render("Your Score is : " + str(score), True, RED)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

    # blit will draw the text on screen
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(4)
    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


# init time and tick settings
start_time = time.time()
fps = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                or event.key == ord("w")
                or event.key == ord("W")
                or event.key == ord("k")
                or event.key == ord("K")
            ):
                change_to = "UP"
            if (
                event.key == pygame.K_DOWN
                or event.key == ord("s")
                or event.key == ord("S")
                or event.key == ord("j")
                or event.key == ord("J")
            ):
                change_to = "DOWN"
            if (
                event.key == pygame.K_LEFT
                or event.key == ord("a")
                or event.key == ord("A")
                or event.key == ord("h")
                or event.key == ord("H")
            ):
                change_to = "LEFT"
            if (
                event.key == pygame.K_RIGHT
                or event.key == ord("d")
                or event.key == ord("D")
                or event.key == ord("l")
                or event.key == ord("L")
            ):
                change_to = "RIGHT"
        else:
            pass

    current_snake_direction = snake.get_direction()
    # here we handle the snake direction change:
    # if the snake is moving in one direction,
    # it cannot change to the opposite direction.
    if change_to == "UP" and current_snake_direction != "DOWN":
        new_snake_direction = "UP"
    if change_to == "DOWN" and current_snake_direction != "UP":
        new_snake_direction = "DOWN"
    if change_to == "LEFT" and current_snake_direction != "RIGHT":
        new_snake_direction = "LEFT"
    if change_to == "RIGHT" and current_snake_direction != "LEFT":
        new_snake_direction = "RIGHT"

    # update the snake body postion based on the direction
    snake.set_direction(new_snake_direction)

    # check if the snake has eaten the food
    # if yes, add the length of the snake and generate new food
    # if no, do nothing and just move the snake

    food_pos = food_controller.get_pos(idx="all")
    snake_head_pos = snake.get_head_pos()

    is_food_eaten = check(food_pos, snake_head_pos)
    if is_food_eaten:
        # get the food eaten based on the index
        eaten_food_idx = food_controller.get_food_at_pos(pos=snake_head_pos)
        eaten_food = food_controller.get_food(idx=eaten_food_idx)

        # update the score and grow the snake
        score += eaten_food.get_score()
        snake.grow(color=eaten_food.color)

        # remove the eaten food and generate a new one
        food_controller.remove(idx=eaten_food_idx)
        food_controller.generate(
            1, snake.get_all_pos(), wall_controller.get_all_collision()
        )
    else:
        snake.move()

    # update screen and draw the snake, food and background
    screen.fill(BLACK)
    food_controller.draw(screen=screen)
    wall_controller.draw(screen=screen)
    snake.draw(screen=screen)

    # Game Over conditions
    snake_head_pos = snake.get_head_pos()
    if snake_head_pos[0] < 0 or snake_head_pos[0] > SCREEN_WIDTH - 10:
        game_over(0)
    if snake_head_pos[1] < 0 or snake_head_pos[1] > SCREEN_HEIGHT - 10:
        game_over(0)

    # Touching the snake body
    if check(snake_head_pos, [block.pos for block in snake.body[-2::-1]]):
        game_over(1)

    if check(snake_head_pos, wall_controller.get_all_collision()):
        game_over(2)

    show_info(
        screen=screen,
        place="upperright",
        score=score,
        time_played=(time.time() - start_time),
    )

    # Refresh game screen
    pygame.display.update()

    # generate a new wall per GENERATE_WALL_INTERVAL
    if (time.time() - start_time) / GENERATE_WALL_INTERVAL > wall_controller.count():
        wall_controller.generate(1, food_controller.get_pos(), snake.get_all_pos())

    # Frame Per Second /Refresh Rate
    # increase snake speed 2 per minute after the first minute
    snake_speed = INITIAL_SNAKE_SPEED + 2 / 60 * max(0, (time.time() - start_time - 1))
    fps.tick(snake_speed)
