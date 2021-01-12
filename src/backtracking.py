from typing import Optional, Any
from src.labyrinth import Labyrinth, Pos


class Backtracking:
    """Build a labyrinth using a backtracking algorithm."""

    def carve(self, lab: Labyrinth, pos: Optional[Pos] = None, show: Any = None):
        """carve passages starting at Pos p using recursive backtracking.

        Carves passages into the labyrinth, starting at Pos p (Default: 0,0),
        using a recursive backtracking algorithm. Uses stack as deeply as the
        longest possible path will be.
        """
        # Set start position
        if not pos:
            pos = Pos((0, 0))

        # probe in random order
        directions = lab.random_directions()
        for d in directions:
            # try to step into this direction
            try:
                np = lab.step(pos, d)
            except ValueError:
                # We stepped off the grid
                continue

            if show:
                show(lab, red=pos, green=np)

            # if the position is clean, make a passage, and recurse
            if lab[np] == 0:
                lab.make_passage(pos, d)
                lab.carve(np, show=show)
