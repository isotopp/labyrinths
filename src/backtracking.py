from typing import Optional
from random import randrange
from src.labyrinth import Labyrinth, Pos


class Backtracking(Labyrinth):
    """Build a labyrinth using a backtracking algorithm."""

    def carve(self, pos: Optional[Pos] = None) -> None:
        """carve passages starting at Pos p using recursive backtracking.

        Carves passages into the labyrinth, starting at Pos p (Default: 0,0),
        using a recursive backtracking algorithm. Uses stack as deeply as the
        longest possible path will be.
        """
        # Set start position
        if not pos:
            pos = Pos((0, 0))

        # probe in random order
        directions = self.random_directions()
        for d in directions:
            # try to step into this direction
            try:
                np = self.step(pos, d)
            except ValueError:
                # We stepped off the grid
                continue

            # if the position is clean, make a passage, and recurse
            if self[np] == 0:
                self.make_passage(pos, d)
                self.carve(np)

    def carve_more(self, walls_to_remove: int = 0):
        """Remove walls_to_remove more walls, randomly.

        After applying carve(), we randomly delete walls_to_remove many more walls
        to create for multiple valid pathes to the goal.

        We guarantee that each new passage is actually a wall removed, and that
        new passages do not lead off the grid.
        """
        to_go = walls_to_remove
        while to_go:
            # Choose a random position and direction
            pos = Pos((randrange(self.width), randrange(self.height)))
            d = self.random_directions()[0]

            # and check if deleting the wall would change things.
            if self.can_make_passage(pos, d):
                # guaranteed to stay on grid and change the world
                self.make_passage(pos, d)
                to_go -= 1  # one done
