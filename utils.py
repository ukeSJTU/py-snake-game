import pygame
from block import Snake, Block, Food, FoodManager
from typing import Union, Tuple, Literal, List
import sys
import time
import random
from colors import *


def draw(surface: pygame.Surface, content: Union[Snake, FoodManager, Food]) -> None:
    if type(content) == Snake:
        # print(f"Draw Snake: {[block.color for block in content.body]}")
        for block in content.body:
            pygame.draw.rect(
                surface,
                block.color,
                (block.pos[0], block.pos[1], block.width, block.height),
            )
    elif type(content) == Food:
        pygame.draw.rect(
            surface,
            content.color,
            (content.pos[0], content.pos[1], content.width, content.height),
        )
    elif type(content) == FoodManager:
        for food in content.get_food(idx="all"):
            pygame.draw.rect(
                surface,
                food.color,
                (food.pos[0], food.pos[1], food.width, food.height),
            )
    return


def show_info(
    screen: pygame.Surface,
    score: int,
    time_played: int,
    place: Literal["upperright", "upperleft", "lowerright", "lowerleft"] = "upperright",
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


def check_collision(
    pos_list_1: Union[Tuple[int, int], List[Tuple[int, int]]],
    pos_list_2: Union[Tuple[int, int], List[Tuple[int, int]]],
) -> Tuple[bool, Union[Tuple[int, int], None]]:
    if type(pos_list_1) == tuple:
        pos_list_1 = [pos_list_1]
    if type(pos_list_2) == tuple:
        pos_list_2 = [pos_list_2]

    # print(f"pos_list_1: {pos_list_1}")
    # print(f"pos_list_2: {pos_list_2}")

    for i in range(len(pos_list_1)):
        for j in range(len(pos_list_2)):
            if pos_list_1[i] == pos_list_2[j]:
                return (True, (i, j))

    return (False, None)
