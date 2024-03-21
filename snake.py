from typing import List, Tuple, Union, Literal
from colors import *
import pygame

from base_class import Block
from type_alias import *


Positon = Tuple[int, int]
Color = Tuple[int, int, int]


class SnakeBodyBlock:
    def __init__(self, pos: Positon, color: Color, width: int, height: int):
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height

    def draw(self: "Block", screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.color,
            (self.pos[0], self.pos[1], self.width, self.height),
        )


# A new class for snake head and tail part
# it basically is same with Block class
# but its appearance change as it has a rounded-border style


class Snake:
    def __init__(
        self,
        body: List[SnakeBodyBlock],
        direction: Direction,
    ):
        self.body = body
        self.direction = direction

        self.head_pos = self.body[-1].pos

        self.isGrowing = False

        # print(self.head_pos)
        # exit(1)

    def get_direction(self: "Snake") -> Direction:
        return self.direction

    def set_direction(self: "Snake", direction: Direction) -> None:
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

        new_snake_head = SnakeBodyBlock(
            pos=self.head_pos, color=WHITE, width=10, height=10
        )
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

    def get_all_pos(self: "Snake") -> List[Positon]:
        return [block.pos for block in self.body]

    def grow(self: "Snake", color: Color = WHITE, width: int = 10, height: int = 10):
        self.isGrowing = True
        self.move()
        self.body[0].color = color

    def draw(self: "Snake", screen: pygame.Surface):
        for block in self.body:
            block.draw(screen)
