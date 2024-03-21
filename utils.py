import pygame
from typing import Union, Tuple, Literal, List
import random

from colors import *
from type_alias import *


def generate_position(grid_width, grid_height, std_dev_factor=0.15) -> Position:

    # Calculate mean and standard deviation
    mean_x = grid_width / 2
    mean_y = grid_height / 2
    std_dev_x = grid_width * std_dev_factor
    std_dev_y = grid_height * std_dev_factor

    # Generate positions using a normal distribution
    # Ensure the generated positions are within the grid boundaries
    x_position = min(max(int(random.gauss(mean_x, std_dev_x)), 0), grid_width - 1)
    y_position = min(max(int(random.gauss(mean_y, std_dev_y)), 0), grid_height - 1)

    # the position should be a multiple of 10
    x_position = x_position - (x_position % 10)
    y_position = y_position - (y_position % 10)

    return (x_position, y_position)


def show_info(
    screen: pygame.Surface,
    score: int,
    time_played: int,
    place: displayPosition = "upperright",
    color: Tuple[int, int, int] = WHITE,
) -> None:
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


def check(*lists):
    # print("check collision: ", lists)
    seen = set()
    for lst in lists:
        if type(lst) != list:
            lst = [lst]
        for item in lst:
            if len(item) == 0:
                continue
            if item in seen:
                return True  # A collision is found
            seen.add(tuple(item))
    return False  # No collisions were found
