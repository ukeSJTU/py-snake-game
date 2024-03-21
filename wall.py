from typing import List, Tuple, Union, Literal
import random
import pygame

from utils import generate_position, check_collision, check
from colors import *
from type_alias import Position, Color
from base_class import Block, Controller


class Wall:
    def __init__(
        self,
        direction: Literal["Horizontal", "Vertical"],
        pos: Position,
        width: int = None,
        height: int = None,
        color: Color = WHITE,
    ):
        """__init__ method for Wall class

        Args:
            direction (Horizontal or Vertical): direction of the wall
            pos (Positon): position of the wall(x, y) in px
            width (int, optional): width of the wall (px). Defaults to None.
            height (int, optional): height of the wall (px). Defaults to None.
            color (Color, optional): color of the wall. Defaults to WHITE.
        """
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

        self.calc_collision_detect_pos()

    def calc_collision_detect_pos(self) -> None:
        assert self.direction in ["Horizontal", "Vertical"], "Invalid direction value"

        self.collision_detect_pos = []

        if self.direction == "Horizontal":
            for i in range(self.pos[0], self.pos[0] + self.width, 10):
                self.collision_detect_pos.append((i, self.pos[1]))
        elif self.direction == "Vertical":
            for i in range(self.pos[1], self.pos[1] + self.height, 10):
                self.collision_detect_pos.append((self.pos[0], i))

    def get_collision_detect_pos(self) -> List[Position]:
        return self.collision_detect_pos

    def draw(self: "Wall", screen: pygame.Surface):
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

    # def __generate(
    #     self, direction: Literal["Vertical", "Horizontal"] = None, pos: Position = None
    # ) -> Wall:
    #     if direction is None:
    #         direction = random.choice(["Vertical", "Horizontal"])
    #     if pos is None:
    #         pos = generate_position(self.width, self.height)
    #     wall = Wall(direction=direction, pos=pos)
    #     return wall

    def add(self, wall: Union[Wall, None] = None) -> None:
        if wall is None:
            wall = self.generate()
        self.walls.append(wall)
        print(f"Wall added at {wall.pos}")

    def generate(self, n: int = 1, *lists) -> Union[Wall, List[Wall]]:
        cnt = 1
        temp_wall_list = []

        while cnt <= n:
            pos = generate_position(self.width, self.height)
            direction = random.choice(["Vertical", "Horizontal"])
            wall = Wall(direction=direction, pos=pos)
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

        # while (
        #     check(
        #         self.get_all_collision(),
        #         lists,
        #     )
        #     == False
        # ) and (cnt <= n):
        #     # if direction is None:
        #     direction = random.choice(["Vertical", "Horizontal"])
        #     # if pos is None:
        #     pos = generate_position(self.width, self.height)
        #     wall = Wall(direction=direction, pos=pos)
        #     self.add(wall)
        #     temp_wall_list.append(wall)
        #     cnt += 1

        return temp_wall_list[0] if n == 1 else temp_wall_list

    def remove(self, idx: int) -> None:
        self.walls.pop(idx)

    def get(self, idx: Union[int, str] = "all") -> Union[Wall, List[Wall]]:
        """get method to get the wall object

        Args:
            idx (Union[int, str], optional): the index of wall to get or "all" to get all walls. Defaults to "all".

        Returns:
            Union[Wall, List[Wall]]: Wall object or list of Wall objects
        """
        if idx == "all":
            return self.walls
        else:
            return self.walls[idx]

    def count(self) -> int:
        return len(self.walls)

    def get_all_collision(self) -> List[Tuple[Position, Position]]:
        collision_detect_pos = []
        for wall in self.walls:
            collision_detect_pos.extend(wall.get_collision_detect_pos())
        return collision_detect_pos

    def draw(self: "WallController", screen: pygame.Surface):
        for wall in self.walls:
            wall.draw(screen)
