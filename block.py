from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Literal
from colors import *


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

        self.head_pos = self.body[0].pos

    def get_direction(self: "Snake") -> Literal["UP", "DOWN", "LEFT", "RIGHT"]:
        return self.direction

    def set_direction(
        self: "Snake", direction: Literal["UP", "DOWN", "LEFT", "RIGHT"]
    ) -> None:
        self.direction = direction

    def move(self: "Snake", distance: int = 10):
        if self.direction == "UP":
            self.head_pos = (self.head_pos[0], self.head_pos[1] - distance)
        elif self.direction == "DOWN":
            self.head_pos = (self.head_pos[0], self.head_pos[1] + distance)
        elif self.direction == "LEFT":
            self.head_pos = (self.head_pos[0] - distance, self.head_pos[1])
        elif self.direction == "RIGHT":
            self.head_pos = (self.head_pos[0] + distance, self.head_pos[1])

        new_snake_head = Block(pos=self.head_pos, color=WHITE, width=10, height=10)
        self.body.insert(0, new_snake_head)
        self.body.pop()

    def get_head_pos(self: "Snake") -> Positon:
        return self.head_pos

    def grow(self: "Snake", color: Color = WHITE, width: int = 10, height: int = 10):
        new_snake_tail = Block(
            pos=self.body[-1].pos, color=color, width=width, height=height
        )
        self.body.append(new_snake_tail)


class Food(Block):
    def __init__(
        self,
        pos: Positon = None,
        color: Color = WHITE,
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
