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

    def carve_more(self, walls_to_remove: int = 0, show: Any = None):
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
                new_pos = self.step(pos, d)

                if show:
                    show(self, red=pos, green=new_pos)

                # guaranteed to stay on grid and change the world
                self.make_passage(pos, d)
                to_go -= 1  # one done
