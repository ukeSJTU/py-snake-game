from typing import List, Tuple, Union, Literal
import random
import pygame

from base_class import Controller
from colors import *
from utils import generate_position, check
from type_alias import *


class Wall:
    def __init__(
        self,
        orientation: Orientation,
        pos: Position,
        width: int = None,
        height: int = None,
        color: Color = WHITE,
    ):
        """__init__ method for Wall class

        Args:
            orientation (Horizontal or Vertical): orientation of the wall
            pos (Positon): position of the wall(x, y) in px
            width (int, optional): width of the wall (px). Defaults to None.
            height (int, optional): height of the wall (px). Defaults to None.
            color (Color, optional): color of the wall. Defaults to WHITE.
        """
        self.orientation = orientation
        self.pos = pos

        if self.orientation == "Horizontal":
            self.width = width if width is not None else 50
            self.height = height if height is not None else 10
        elif self.orientation == "Vertical":
            self.width = width if width is not None else 10
            self.height = height if height is not None else 50
        else:
            raise ValueError(
                "Invalid orientation value. Must be 'Horizontal' or 'Vertical'."
            )

        self.color = color

        self.calc_collision_detect_pos()

    def calc_collision_detect_pos(self) -> None:
        """Calculate the collision detection positions of the wall"""
        assert self.orientation in [
            "Horizontal",
            "Vertical",
        ], "Invalid orientation value"

        self.collision_detect_pos = []

        if self.orientation == "Horizontal":
            for i in range(self.pos[0], self.pos[0] + self.width, 10):
                self.collision_detect_pos.append((i, self.pos[1]))
        elif self.orientation == "Vertical":
            for i in range(self.pos[1], self.pos[1] + self.height, 10):
                self.collision_detect_pos.append((self.pos[0], i))

    def get_collision_detect_pos(self) -> List[Position]:
        """Get the collision detection positions of the wall

        Returns:
            List[Position]: list of collision detection positions of the wall
        """
        return self.collision_detect_pos

    def draw(self: "Wall", screen: pygame.Surface):
        """Draw the wall on the screen"""
        pygame.draw.rect(
            screen,
            self.color,
            (self.pos[0], self.pos[1], self.width, self.height),
        )


class WallController(Controller):
    def __init__(self, walls: Union[List[Wall], None], width: int, height: int):
        """WallController class to manage all the walls in the game

        Args:
            walls (Union[List[Wall], None]): list of walls
            width (int): width of the game window
            height (int): height of the game window
        """
        self.walls = [] if walls is None else walls
        self.width = width
        self.height = height

    def add(self, wall: Union[Wall, None] = None) -> None:
        """Add a wall to the list of walls

        Args:
            wall (Union[Wall, None], optional): wall(s) to add to the wallcontroller. Defaults to None.
        """
        if wall is None:
            wall = self.generate()
        self.walls.append(wall)
        print(f"Wall added at {wall.pos}")

    def generate(self, n: int = 1, *lists) -> Union[Wall, List[Wall]]:
        """Generate and add new walls to the list of walls

        Args:
            n (int, optional): number of wall(s) to generate. Defaults to 1.

        Returns:
            Union[Wall, List[Wall]]: generated wall(s), a single wall if n=1, else a list of walls
        """
        cnt = 1
        temp_wall_list = []

        while cnt <= n:
            pos = generate_position(self.width, self.height)
            orientation = random.choice(["Vertical", "Horizontal"])
            wall = Wall(orientation=orientation, pos=pos)
            if (
                check(
                    wall.get_collision_detect_pos(),
                    lists[0],
                )
                == False
            ):
                self.add(wall)
                temp_wall_list.append(wall)
                cnt += 1

        return temp_wall_list[0] if n == 1 else temp_wall_list

    def remove(self, idx: int) -> None:
        """Remove a wall from the list of walls"""
        self.walls.pop(idx)

    def get(self, idx: Union[int, str] = "all") -> Union[Wall, List[Wall]]:
        """Get a wall from the list of walls

        Args:
            idx (Union[int, str], optional): the index of the wall. Defaults to "all".

        Returns:
            Union[Wall, List[Wall]]: the wall at the specified index
        """
        if idx == "all":
            return self.walls
        else:
            return self.walls[idx]

    def count(self) -> int:
        """Get the number of walls in the list"""
        return len(self.walls)

    def get_all_collision(self) -> List[Tuple[Position, Position]]:
        """Get all collision detection positions of the walls

        Returns:
            List[Tuple[Position, Position]]: list of collision detection positions of the walls
        """
        collision_detect_pos = []
        for wall in self.walls:
            collision_detect_pos.extend(wall.get_collision_detect_pos())
        return collision_detect_pos

    def draw(self: "WallController", screen: pygame.Surface):
        """Draw all the walls on the screen"""
        for wall in self.walls:
            wall.draw(screen)
