import pygame
from block import Snake, Block, Food
from typing import Union, Tuple
import sys
import time
import random
from colors import *
from utils import *
from block import FoodManager, WallController

# set window size and name
screen_width, screen_height = 800, 800

# initial score
score = 0

# initial speed
initial_snake_speed = 10

window_caption = "USerName-蛇吃豆-UserID"


init_snake_direction = "RIGHT"
snake_direction = init_snake_direction
change_to = snake_direction


# initialize the pygame
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(window_caption)

snake = Snake(
    body=[
        Block(pos=(390, 390), color=WHITE, width=10, height=10),
        Block(pos=(400, 390), color=WHITE, width=10, height=10),
    ],
    direction=init_snake_direction,
)

fps = pygame.time.Clock()

food_manager = FoodManager(
    # width=screen_width,
    # height=screen_height,
    width=400,
    height=400,
)
food_manager.generate()

wall_controller = WallController(walls=None, width=screen_width, height=screen_height)
wall_controller.add()


# game over function
def game_over(code: int):
    if code == 0:
        print("Game Over because of collision with the wall")
    elif code == 1:
        print("Game Over because of collision with the snake body")
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
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)

    # blit will draw the text on screen
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(1)
    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


start_time = time.time()
while True:
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                or event.key == ord("w")
                or event.key == ord("W")
            ):
                change_to = "UP"
            if (
                event.key == pygame.K_DOWN
                or event.key == ord("s")
                or event.key == ord("S")
            ):
                change_to = "DOWN"
            if (
                event.key == pygame.K_LEFT
                or event.key == ord("a")
                or event.key == ord("A")
            ):
                change_to = "LEFT"
            if (
                event.key == pygame.K_RIGHT
                or event.key == ord("d")
                or event.key == ord("D")
            ):
                change_to = "RIGHT"
        else:
            pass

    current_snake_direction = snake.get_direction()
    # If two keys pressed simultaneously
    # we don't want snake to move into two directions
    # simultaneously
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
    # if no, do nothing

    food_pos = food_manager.get_pos(idx="all")
    snake_head_pos = snake.get_head_pos()

    is_food_eaten, idx = check_collision(pos_list_1=food_pos, pos_list_2=snake_head_pos)
    if is_food_eaten:
        eaten_food = food_manager.get_food(idx=idx[0] + idx[1] - 0)
        score += eaten_food.get_score()
        # new_color = food.color
        print(f"Food id={idx[0] + idx[1] - 0} color={eaten_food.color}")
        snake.grow(color=eaten_food.color)
        food_manager.remove(idx=idx[0] + idx[1] - 0)
        food_manager.generate()
    else:
        snake.move()

    # update screen and draw the snake, food and background
    screen.fill(BLACK)
    draw(surface=screen, content=snake)

    draw(surface=screen, content=food_manager)

    draw(surface=screen, content=wall_controller)

    snake_head_pos = snake.get_head_pos()
    # Game Over conditions
    if snake_head_pos[0] < 0 or snake_head_pos[0] > screen_width - 10:
        game_over(0)
    if snake_head_pos[1] < 0 or snake_head_pos[1] > screen_height - 10:
        game_over(0)

    # Touching the snake body
    if check_collision(
        pos_list_1=snake_head_pos,
        pos_list_2=[block.pos for block in snake.body[-2::-1]],
    )[0]:
        game_over(1)

    show_info(
        screen=screen,
        place="upperright",
        score=score,
        time_played=(time.time() - start_time),
    )

    # Refresh game screen
    pygame.display.update()

    # generate a new wall every one minute
    if (time.time() - start_time) / 10 > wall_controller.count():
        wall_controller.add()
        # start_time = time.time()

    # Frame Per Second /Refresh Rate
    # increase snake speed 2 per minute after the first minute
    snake_speed = initial_snake_speed + 2 / 60 * max(0, (time.time() - start_time - 1))
    fps.tick(snake_speed)
