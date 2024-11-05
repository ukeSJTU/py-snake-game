from typing import List, Tuple, Union, Literal
import pygame

from base_class import Block
from colors import *
from type_alias import *


class SnakeBodyBlock:
    def __init__(self, pos: Position, color: Color, width: int, height: int):
        """Body block of the snake

        Args:
            pos (Position): position of the snake body block (px)
            color (Color): color of the snake body block
            width (int): width of the snake body block (px)
            height (int): height of the snake body block (px)
        """
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height

    def draw(self: "Block", screen: pygame.Surface):
        """Draw the block on the screen

        Args:
            self (Block): block
            screen (pygame.Surface): screen to draw the block
        """
        pygame.draw.rect(
            screen,
            self.color,
            (self.pos[0], self.pos[1], self.width, self.height),
        )


class Snake:
    def __init__(
        self,
        body: List[SnakeBodyBlock],
        direction: Direction,
    ):
        """__init__ method for Snake Class

        Args:
            body (List[SnakeBodyBlock]): the body of the snake
            direction (Direction): the direction of the snake
        """
        self.body = body
        self.direction = direction

        self.head_pos = self.body[-1].pos

        self.isGrowing = False

    def get_direction(self: "Snake") -> Direction:
        """Get the direction of the snake

        Args:
            self (Snake): Snake object

        Returns:
            Direction: direction of the snake
        """
        return self.direction

    def set_direction(self: "Snake", direction: Direction) -> None:
        """Set the direction of the snake

        Args:
            self (Snake): Snake object
            direction (Direction): direction to set
        """
        self.direction = direction

    def move(self: "Snake", distance: int = 10):
        """Move the snake in the current direction

        Args:
            self (Snake): Snake object
            distance (int, optional): distance to move. Defaults to 10.
        """
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
            pos=self.head_pos,
            color=WHITE,
            width=10,
            height=10,
        )
        self.body.append(new_snake_head)

        # move the color of the snake to the next block
        for idx in range(len(self.body) - 1, 0, -1):
            self.body[idx].color = self.body[idx - 1].color

        if not self.isGrowing:
            self.body.pop(0)
        else:
            self.isGrowing = False

    def get_head_pos(self: "Snake") -> Position:
        """Get the position of the snake's head

        Args:
            self (Snake): Snake object

        Returns:
            Position: position of the snake's head
        """
        return self.head_pos

    def get_all_pos(self: "Snake") -> List[Position]:
        """Get the positions of all blocks in the snake's body

        Args:
            self (Snake): Snake object

        Returns:
            List[Position]: list of positions of all blocks in the snake's body
        """
        return [block.pos for block in self.body]

    def grow(self: "Snake", color: Color = WHITE, width: int = 10, height: int = 10):
        """Make the snake grow by adding a new block

        Args:
            self (Snake): Snake object
            color (Color, optional): color of the new block. Defaults to WHITE.
            width (int, optional): width of the new block (px). Defaults to 10.
            height (int, optional): height of the new block (px). Defaults to 10.
        """
        self.isGrowing = True
        self.move()
        self.body[0].color = color

    def draw(self: "Snake", screen: pygame.Surface):
        """Draw the snake on the screen

        Args:
            self (Snake): Snake object
            screen (pygame.Surface): screen to draw the snake
        """
        for block in self.body:
            block.draw(screen)
