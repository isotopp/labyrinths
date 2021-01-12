from typing import Any, Optional
from random import choice, randrange
from src.labyrinth import Labyrinth, Pos, Direction


class BinaryTree:
    """Build a labyrinth using a backtracking algorithm."""

    def carve(self, lab: Labyrinth, pos: Optional[Pos] = None, show: Any = None):
        """carve passages starting at Pos p using binary tree algo.
        """
        for y in range(0, lab.height):
            for x in range(0, lab.width):
                pos = Pos((x, y))
                candidates = []
                if lab.can_make_passage(pos, Direction("N")):
                    candidates.append(Direction("N"))
                if lab.can_make_passage(pos, Direction("E")):
                    candidates.append(Direction("E"))

                try:
                    d = choice(candidates)
                except IndexError:
                    continue
                lab.make_passage(pos, d)

                if show:
                    np = lab.step(pos, d)
                    show(lab, red=pos, green=np)
