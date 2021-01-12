from typing import Any
from random import choice, randrange
from src.labyrinth import Labyrinth, Pos, Direction


class BinaryTree(Labyrinth):
    """Build a labyrinth using a backtracking algorithm."""

    def carve(self, show: Any = None) -> None:
        """carve passages starting at Pos p using binary tree algo.
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = Pos((x, y))
                candidates = []
                if self.can_make_passage(pos, Direction("N")):
                    candidates.append(Direction("N"))
                if self.can_make_passage(pos, Direction("E")):
                    candidates.append(Direction("E"))

                try:
                    d = choice(candidates)
                except IndexError:
                    continue
                self.make_passage(pos, d)

                if show:
                    np = self.step(pos, d)
                    show(self, red=pos, green=np)
