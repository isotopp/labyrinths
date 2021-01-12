from typing import Any
from random import choice, randrange
from src.labyrinth import Labyrinth, Pos, Direction


class Sidewinder(Labyrinth):
    """Build a labyrinth using a backtracking algorithm."""

    def carve(self, show: Any = None) -> None:
        """carve passages starting at Pos p using sidewinder algo."""
        for y in range(0, self.height):
            run = []
            for x in range(0, self.width):
                pos = Pos((x, y))
                run.append(pos)

                at_eastern_boundary = x+1 == self.width
                at_northern_boundary = y == 0

                should_close_out = at_eastern_boundary or (not at_northern_boundary and randrange(2) == 0)

                if should_close_out:
                    member = choice(run)
                    if self.can_make_passage(member, Direction("N")):
                        self.make_passage(member, Direction("N"))
                    run = []
                    if show:
                        show(self, red=pos, green=member)
                else:
                    if self.can_make_passage(pos, Direction("E")):
                        np = self.step(pos, Direction("E"))
                        self.make_passage(pos, Direction("E"))
                        if show:
                            show(self, red=pos, green=np)
