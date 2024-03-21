from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Literal
import pygame
import itertools

from base_class import Block, Controller
from utils import generate_position, check
from colors import *
from type_alias import Position, Color


class Food(Block):
    def __init__(
        self,
        pos: Position = None,
        color: Color = COLOR_LIST[0],
        score: int = 10,
        width: int = 10,
        height: int = 10,
    ):
        """__init__ method for Food class

        Args:
            pos (Positon, optional): position of food instance. Defaults to None.
            color (Color, optional): color of food instance. Defaults to COLOR_LIST[0].
            score (int, optional): score of food instance. Defaults to 10.
            width (int, optional): width of food instance in px. Defaults to 10px.
            height (int, optional): height of food instance in px. Defaults to 10px.
        """
        super().__init__(pos, color, width, height)
        self.score = score

    def get_pos(self: "Food") -> Position:
        return self.pos

    def get_score(self: "Food") -> int:
        return self.score

    def draw(self: "Food", screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.color,
            (self.pos[0], self.pos[1], self.width, self.height),
        )


# a class to monitor and control all the food in the game
class FoodController(Controller):

    def __init__(
        self,
        width: int,
        height: int,
        color_list: List[Color] = [WHITE, YELLOW, RED, ORANGE, BLUE, GREEN],
        score_list: List[int] = [10, 20, 30, 40, 50, 60],
        food_list: List[Food] = [],
    ):
        """FoodController class to manage all the food in the game

        Args:
            width (int): width of the game window
            height (int): height of the game window or
            color_list (List[Color], optional): the list of colors to choose from. Defaults to [WHITE, YELLOW, RED, ORANGE, BLUE, GREEN].
            score_list (List[int], optional): the list of scores for each type of food. Defaults to [10, 20, 30, 40, 50, 60].
            food_list (List[Food], optional): exisiting food list. Defaults to [].
        """
        self.width = width
        self.height = height

        self.colors = self.__repeatable_generator(color_list)
        self.scores = self.__repeatable_generator(score_list)
        self.foods = food_list

        self.color = self.__next_color()
        self.score = self.__next_score()

        self.food_cnt = len(self.foods)

    def __repeatable_generator(self, iterable: List):
        cycle_iterator = itertools.cycle(iterable)
        while True:
            yield next(cycle_iterator)

    def add(self, food: Food) -> None:
        self.foods.append(food)
        self.food_cnt += 1
        print(f"Food added at {food.get_pos()}")

    def generate(self, n: int = 1, *lists) -> Union[Food, List[Food]]:
        print(lists)

        temp_food_list = []
        cnt = 1
        while cnt <= n:
            position = generate_position(self.width, self.height)

            if (
                check(
                    position,
                    lists[0],
                )
                == False
            ):
                new_food = Food(
                    pos=position,
                    color=self.color,
                    score=self.score,
                    width=10,
                    height=10,
                )
                self.add(new_food)
                temp_food_list.append(new_food)
                cnt += 1
                self.update()

        return temp_food_list

    def get(self, idx: Union[int, str] = "all") -> Union[Food, List[Food]]:
        if idx == "all":
            return self.foods
        else:
            return self.foods[idx]

    def __next_color(self) -> Color:
        self.color = next(self.colors)
        return self.color

    def __next_score(self) -> int:
        self.score = next(self.scores)
        return self.score

    def update(self) -> Tuple[Color, int]:
        return (self.__next_color(), self.__next_score())

    def count(self) -> int:
        return self.food_cnt

    def get_pos(self, idx: Union[int, str] = "all") -> Union[Position, List[Position]]:
        if idx == "all":
            return [food.get_pos() for food in self.foods]
        else:
            return self.foods[idx].get_pos()

    def get_food(self, idx: Union[int, str] = "all") -> Food:
        if idx == "all":
            return self.foods
        else:
            return self.foods[idx]

    def remove(self, idx: int) -> None:
        self.foods.pop(idx)
        self.food_cnt -= 1

    def draw(self: "FoodController", screen: pygame.Surface):
        for food in self.foods:
            food.draw(screen)
