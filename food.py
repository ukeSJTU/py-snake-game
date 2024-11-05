from typing import List, Tuple, Union, Literal
import pygame
import itertools

from base_class import Block, Controller
from utils import generate_position, check
from colors import *
from type_alias import *


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
        """Get the position of the food instance.

        Returns:
            Position: The position of the food instance.
        """
        return self.pos

    def get_score(self: "Food") -> int:
        """Get the score of the food instance.

        Returns:
            int: The score of the food instance.
        """
        return self.score

    def draw(self: "Food", screen: pygame.Surface):
        """Draw the food instance on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the food on.
        """
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
        """A generator that repeats the elements of an iterable indefinitely.

        Args:
            iterable (List): The iterable to repeat.

        Yields:
            Any: The next element from the iterable.
        """
        cycle_iterator = itertools.cycle(iterable)
        while True:
            yield next(cycle_iterator)

    def add(self, food: Food) -> None:
        """Add a food instance to the food list.

        Args:
            food (Food): The food instance to add.
        """
        self.foods.append(food)
        self.food_cnt += 1
        print(f"Food added at {food.get_pos()}")

    def generate(self, n: int = 1, *lists) -> Union[Food, List[Food]]:
        """Generate new food instances.

        Args:
            n (int, optional): The number of food instances to generate. Defaults to 1.
            *lists: Variable number of lists.

        Returns:
            Union[Food, List[Food]]: The generated food instance(s).
        """
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
        """Get the food instance(s) at the specified index.

        Args:
            idx (Union[int, str], optional): The index of the food instance to get. Defaults to "all".

        Returns:
            Union[Food, List[Food]]: The food instance(s) at the specified index.
        """
        if idx == "all":
            return self.foods
        else:
            return self.foods[idx]

    def __next_color(self) -> Color:
        """Get the next color from the color generator.

        Returns:
            Color: The next color.
        """
        self.color = next(self.colors)
        return self.color

    def __next_score(self) -> int:
        """Get the next score from the score generator.

        Returns:
            int: The next score.
        """
        self.score = next(self.scores)
        return self.score

    def update(self) -> Tuple[Color, int]:
        """Update the color and score for the next food instance.

        Returns:
            Tuple[Color, int]: The updated color and score.
        """
        return (self.__next_color(), self.__next_score())

    def count(self) -> int:
        """Get the number of food instances.

        Returns:
            int: The number of food instances.
        """
        return self.food_cnt

    def get_pos(self, idx: Union[int, str] = "all") -> Union[Position, List[Position]]:
        """Get the position(s) of the food instance(s) at the specified index.

        Args:
            idx (Union[int, str], optional): The index of the food instance. Defaults to "all".

        Returns:
            Union[Position, List[Position]]: The position(s) of the food instance(s).
        """
        if idx == "all":
            return [food.get_pos() for food in self.foods]
        else:
            return self.foods[idx].get_pos()

    def get_food(self, idx: Union[int, str] = "all") -> Food:
        """Get the food instance(s) at the specified index.

        Args:
            idx (Union[int, str], optional): The index of the food instance. Defaults to "all".

        Returns:
            Food: The food instance(s) at the specified index.
        """
        if idx == "all":
            return self.foods
        else:
            return self.foods[idx]

    def remove(self, idx: int) -> None:
        """Remove the food instance at the specified index.

        Args:
            idx (int): The index of the food instance to remove.
        """
        self.foods.pop(idx)
        self.food_cnt -= 1

    def draw(self: "FoodController", screen: pygame.Surface):
        """Draw all the food instances on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the food on.
        """
        for food in self.foods:
            food.draw(screen)

    def get_food_at_pos(self, pos: Position) -> Union[int, None]:
        """Get the index of the food instance at the specified position.

        Args:
            pos (Position): The position to check.

        Returns:
            Union[int, None]: The index of the food instance at the specified position, or None if not found.
        """
        for idx in range(len(self.foods)):
            if self.foods[idx].get_pos() == pos:
                return idx

        return None
