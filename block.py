from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Literal
from colors import *
import random
import itertools


Positon = Tuple[int, int]
Color = Tuple[int, int, int]


class Block:
    def __init__(self, pos: Positon, color: Color, width: int, height: int):
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height


class Snake:
    def __init__(
        self,
        body: List[Block],
        direction: Literal["UP", "DOWN", "LEFT", "RIGHT"],
    ):
        self.body = body
        self.direction = direction

        self.head_pos = self.body[-1].pos

        self.isGrowing = False

        # print(self.head_pos)
        # exit(1)

    def get_direction(self: "Snake") -> Literal["UP", "DOWN", "LEFT", "RIGHT"]:
        return self.direction

    def set_direction(
        self: "Snake", direction: Literal["UP", "DOWN", "LEFT", "RIGHT"]
    ) -> None:
        self.direction = direction

    def move(self: "Snake", distance: int = 10):
        self.head_pos = self.body[-1].pos
        if self.direction == "UP":
            self.head_pos = (self.head_pos[0], self.head_pos[1] - distance)
        elif self.direction == "DOWN":
            self.head_pos = (self.head_pos[0], self.head_pos[1] + distance)
        elif self.direction == "LEFT":
            self.head_pos = (self.head_pos[0] - distance, self.head_pos[1])
        elif self.direction == "RIGHT":
            self.head_pos = (self.head_pos[0] + distance, self.head_pos[1])

        new_snake_head = Block(pos=self.head_pos, color=WHITE, width=10, height=10)
        self.body.append(new_snake_head)

        # move the color of the snake to the next block
        for idx in range(len(self.body) - 1, 0, -1):
            self.body[idx].color = self.body[idx - 1].color

        if not self.isGrowing:
            self.body.pop(0)
        else:
            self.isGrowing = False

    def get_head_pos(self: "Snake") -> Positon:
        return self.head_pos

    def grow(self: "Snake", color: Color = WHITE, width: int = 10, height: int = 10):
        self.isGrowing = True
        self.move()
        self.body[0].color = color


class Food(Block):
    COLOR_LIST = [WHITE, YELLOW, RED, ORANGE, BLUE, GREEN]

    def __init__(
        self,
        pos: Positon = None,
        color: Color = COLOR_LIST[0],
        score: int = 10,
        width: int = 10,
        height: int = 10,
    ):
        super().__init__(pos, color, width, height)
        self.score = score

    def get_pos(self: "Food") -> Positon:
        return self.pos

    def get_score(self: "Food") -> int:
        return self.score

    def next(self: "Food", screen_width: int, screen_height: int) -> None:
        self.pos = (
            random.randrange(1, (screen_width // 10)) * 10,
            random.randrange(1, (screen_height // 10)) * 10,
        )
        # next color from the list: WHITE->YELLOW->RED->ORANGE->BLUE->GREEN
        self.color = self.COLOR_LIST[
            (self.COLOR_LIST.index(self.color) + 1) % len(self.COLOR_LIST)
        ]
        self.score = 10 * (self.COLOR_LIST.index(self.color) + 1)


# a class to monitor and control all the food in the game
class FoodManager:

    def __init__(
        self,
        width: int,
        height: int,
        color_list: List[Color] = [WHITE, YELLOW, RED, ORANGE, BLUE, GREEN],
        score_list: List[int] = [10, 20, 30, 40, 50, 60],
        food_list: List[Food] = [],
    ):
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

    def generate(self):
        new_position_x = random.randrange(1, (self.width // 10)) * 10
        new_position_y = random.randrange(1, (self.height // 10)) * 10

        _ = self.update()

        new_food = Food(
            pos=(new_position_x, new_position_y),
            color=self.color,
            score=self.score,
            width=10,
            height=10,
        )
        self.foods.append(new_food)
        self.food_cnt += 1

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

    def get_pos(self, idx: Union[int, str] = "all") -> Union[Positon, List[Positon]]:
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


class Wall:
    def __init__(
        self,
        direction: Literal["Horizontal", "Vertical"],
        pos: Positon,
        width: int = None,
        height: int = None,
        color: Color = WHITE,
    ):
        self.direction = direction
        self.pos = pos

        if self.direction == "Horizontal":
            self.width = width if width is not None else 50
            self.height = height if height is not None else 10
        elif self.direction == "Vertical":
            self.width = width if width is not None else 10
            self.height = height if height is not None else 50
        else:
            raise ValueError(
                "Invalid direction value. Must be 'Horizontal' or 'Vertical'."
            )

        self.color = color

        # the self.pos is the coordinate of the top-left corner of the wall
        # calculate the coordinate of the bottom-right corner of the wall


class WallController:
    def __init__(self, walls: Union[List[Wall], None], width: int, height: int):
        self.walls = [] if walls is None else walls
        self.width = width
        self.height = height

    def __generate(
        self, direction: Literal["Vertical", "Horizontal"] = None, pos: Positon = None
    ) -> Wall:
        if direction is None:
            direction = random.choice(["Vertical", "Horizontal"])
        if pos is None:
            pos = (
                random.randrange(1, (self.width // 10)) * 10,
                random.randrange(1, (self.height // 10)) * 10,
            )
        wall = Wall(direction=direction, pos=pos)
        return wall

    def add(self, wall: Union[Wall, None] = None) -> None:
        if wall is None:
            wall = self.__generate()
        self.walls.append(wall)
        print(f"Wall added at {wall.pos}")

    def remove(self, idx: int) -> None:
        self.walls.pop(idx)

    def get(self, idx: Union[int, str] = "all") -> Union[Wall, List[Wall]]:
        if idx == "all":
            return self.walls
        else:
            return self.walls[idx]

    def count(self) -> int:
        return len(self.walls)
