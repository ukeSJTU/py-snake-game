from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Literal

from colors import *
from type_alias import Position, Color


class Block(ABC):
    def __init__(self, pos: Position, color: Color, width: int, height: int):
        """__init__ method for Block class

        Args:
            pos (Positon): position of the block(x, y) in px
            color (Color): color of the block in RGB
            width (int): width of the block (px)
            height (int): height of the block (px)
        """

        self.pos = pos
        self.color = color
        self.width = width
        self.height = height

    @abstractmethod
    def draw(self):
        pass


class Controller(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    # CRUD
    @abstractmethod
    def add(self, content: Block):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def get(self, idx):
        pass

    # @abstractmethod
    # def remove(self, idx: int):
    #     pass

    # @abstractmethod
    # def get_all_collision(self):
    #     pass/
