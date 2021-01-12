from typing import Any, Optional
from random import choice, randrange
from src.labyrinth import Labyrinth, Pos, Direction


class Sidewinder:
    """Build a labyrinth using a backtracking algorithm."""

    def carve(self, lab: Labyrinth, pos: Optional[Pos] = None, show: Any = None):
        """carve passages starting at Pos p using sidewinder algo."""
        for y in range(0, lab.height):
            run = []
            for x in range(0, lab.width):
                pos = Pos((x, y))
                run.append(pos)

                at_eastern_boundary = x+1 == lab.width
                at_northern_boundary = y == 0

                should_close_out = at_eastern_boundary or (not at_northern_boundary and randrange(2) == 0)

                if should_close_out:
                    member = choice(run)
                    if lab.can_make_passage(member, Direction("N")):
                        lab.make_passage(member, Direction("N"))
                    run = []
                    if show:
                        show(lab, red=pos, green=member)
                else:
                    if lab.can_make_passage(pos, Direction("E")):
                        np = lab.step(pos, Direction("E"))
                        lab.make_passage(pos, Direction("E"))
                        if show:
                            show(lab, red=pos, green=np)
