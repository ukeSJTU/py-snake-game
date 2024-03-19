import pygame
from block import Snake, Block, Food
from typing import Union, Tuple
import sys
import time
import random
from colors import *

# initialize the pygame
pygame.init()
pygame.font.init()

# set window size and name
screen_width, screen_height = 800, 800

# initial score
score = 0


init_snake_direction = "RIGHT"
snake_direction = init_snake_direction
change_to = snake_direction

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("UserName-蛇吃豆-UserID")

snake = Snake(
    body=[
        Block(pos=(390, 390), color=WHITE, width=10, height=10),
        Block(pos=(400, 390), color=WHITE, width=10, height=10),
    ],
    direction=init_snake_direction,
)

fps = pygame.time.Clock()
snake_speed = 10


def draw(surface: pygame.Surface, content: Union[Snake, Food]):

    if type(content) == Snake:
        print(f"Draw Snake: {[block.color for block in content.body]}")
        for block in content.body:
            pygame.draw.rect(
                surface,
                block.color,
                (block.pos[0], block.pos[1], block.width, block.height),
            )
    elif type(content == Food):
        pygame.draw.rect(
            surface,
            content.color,
            (content.pos[0], content.pos[1], content.width, content.height),
        )
    return


# displaying Score function
def show_score(choice, color, font, size):

    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # score_surface
    score_surface = score_font.render("Score : " + str(score), True, color)

    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()

    # displaying text
    screen.blit(score_surface, score_rect)


def show_info(
    screen, place, score: int, time_played: int, color: Tuple[int, int, int] = WHITE
):
    # show score and time played on the upperright corner (place)
    font = pygame.font.SysFont("times new roman", 20)

    score_text = f"Score: {score}"
    score_surface = font.render(score_text, True, color)
    score_rect = score_surface.get_rect()

    time_text = f"Time Played: {time_played:.0f}s"
    time_played_surface = font.render(time_text, True, color)
    time_rect = time_played_surface.get_rect()

    # Position the text surfaces based on 'place'
    if place == "upperright":
        score_rect.topright = (screen.get_width() - 10, 10)
        time_rect.topright = (screen.get_width() - 10, 40)
    elif place == "upperleft":
        score_rect.topleft = (10, 10)
        time_rect.topleft = (10, 40)
    elif place == "lowerright":
        score_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)
        time_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 40)
    elif place == "lowerleft":
        score_rect.bottomleft = (10, screen.get_height() - 10)
        time_rect.bottomleft = (10, screen.get_height() - 40)
    else:
        # Default to upperright if place is not recognized
        score_rect.topright = (screen.get_width() - 10, 10)
        time_rect.topright = (screen.get_width() - 10, 40)

    # Blit the text surfaces onto the screen
    screen.blit(score_surface, score_rect)
    screen.blit(time_played_surface, time_rect)


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

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


def generate_new_food(food: Food):
    # generate new food at random position without colliding with snake
    food.next(screen_width, screen_height)

    return


food = Food(
    pos=(
        random.randrange(1, (screen_width // 10)) * 10,
        random.randrange(1, (screen_height // 10)) * 10,
    ),
    color=WHITE,
    width=10,
    height=10,
    score=10,
)

running = True
start_time = time.time()
while running:
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

    food_pos = food.get_pos()
    snake_head_pos = snake.get_head_pos()

    if snake_head_pos == food_pos:
        score += food.get_score()
        new_color = food.color
        snake.grow(color=new_color)
        generate_new_food(food)
    else:
        snake.move()

    # update screen and draw the snake, food and background
    screen.fill(BLACK)
    draw(surface=screen, content=snake)

    draw(surface=screen, content=food)

    snake_head_pos = snake.get_head_pos()
    # Game Over conditions
    if snake_head_pos[0] < 0 or snake_head_pos[0] > screen_width - 10:
        game_over(0)
    if snake_head_pos[1] < 0 or snake_head_pos[1] > screen_height - 10:
        game_over(0)

    # Touching the snake body
    for block in snake.body[-2::-1]:
        if snake_head_pos[0] == block.pos[0] and snake_head_pos[1] == block.pos[1]:
            game_over(1)

    # displaying score continuously
    # show_score(1, WHITE, "times new roman", 20)

    show_info(
        screen=screen,
        place="upperright",
        score=score,
        time_played=(time.time() - start_time),
    )

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
