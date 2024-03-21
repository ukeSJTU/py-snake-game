import pygame
import sys
import time

from base_class import Block
from colors import *
from utils import *
from food import FoodController
from wall import WallController
from snake import Snake, SnakeBodyBlock

# set window size and name
screen_width, screen_height = 800, 800

# initial score
score = 0

# initial speed
initial_snake_speed = 10
initial_snake_color = WHITE

generate_new_wall_interval = 10  # seconds

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
        SnakeBodyBlock(pos=(390, 390), color=initial_snake_color, width=10, height=10),
        SnakeBodyBlock(pos=(400, 390), color=initial_snake_color, width=10, height=10),
    ],
    direction=init_snake_direction,
)

fps = pygame.time.Clock()


def generate(content_type: Literal["food", "wall"], n: int = 1):
    # generate n food or wall, if the generated position is not valid, regenerate

    cnt = 1
    if content_type == "food":
        for _ in range(n):
            while (
                check_collision(
                    pos_list_1=snake.get_all_pos(),
                    pos_list_2=food_controller.get_pos(idx="all"),
                )[0]
                == False
            ) and (cnt <= n):
                food_controller.generate()
                cnt += 1

    elif content_type == "wall":
        for _ in range(n):
            while (
                check_collision(
                    pos_list_1=snake.get_all_pos(),
                    pos_list_2=wall_controller.get_all_collision(),
                )[0]
                == False
            ) and (cnt <= n):
                wall_controller.add()
                cnt += 1
    else:
        pass


food_controller = FoodController(
    width=screen_width,
    height=screen_height,
)
# food_manager.generate()
# generate(content_type="food", n=1)
food_controller.generate(1, snake.get_all_pos())

wall_controller = WallController(walls=None, width=screen_width, height=screen_height)
wall_controller.generate(1, food_controller.get_pos(), snake.get_all_pos())


# wall_controller.add()
# generate(content_type="wall", n=1)


# game over function
def game_over(code: int):
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

    food_pos = food_controller.get_pos(idx="all")
    snake_head_pos = snake.get_head_pos()

    is_food_eaten, idx = check_collision(pos_list_1=food_pos, pos_list_2=snake_head_pos)
    if is_food_eaten:
        eaten_food = food_controller.get_food(idx=idx[0] + idx[1] - 0)
        score += eaten_food.get_score()
        # new_color = food.color
        print(f"Food id={idx[0] + idx[1] - 0} color={eaten_food.color}")
        snake.grow(color=eaten_food.color)
        food_controller.remove(idx=idx[0] + idx[1] - 0)
        # food_manager.generate()
        # generate(content_type="food", n=1)
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

    if check_collision(
        pos_list_1=snake_head_pos, pos_list_2=wall_controller.get_all_collision()
    )[0]:
        game_over(2)

    show_info(
        screen=screen,
        place="upperright",
        score=score,
        time_played=(time.time() - start_time),
    )

    # Refresh game screen
    pygame.display.update()

    # generate a new wall every one minute
    if (
        time.time() - start_time
    ) / generate_new_wall_interval > wall_controller.count():
        wall_controller.generate(1, food_controller.get_pos(), snake.get_all_pos())
        # generate(content_type="wall", n=1)
        # start_time = time.time()

    # Frame Per Second /Refresh Rate
    # increase snake speed 2 per minute after the first minute
    snake_speed = initial_snake_speed + 2 / 60 * max(0, (time.time() - start_time - 1))
    fps.tick(snake_speed)
