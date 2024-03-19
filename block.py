from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Literal
from colors import *
import random


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
