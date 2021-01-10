from typing import Optional, Any
from random import randrange
from src.labyrinth import Labyrinth, Pos


class DepthFirst(Labyrinth):
    """Build a labyrinth using a backtracking algorithm."""

    def carve(self, pos: Optional[Pos] = None, show: Any = None) -> None:
        """carve passages starting at Pos p using recursive backtracking.

        Carves passages into the labyrinth, starting at Pos p (Default: 0,0),
        using a recursive backtracking algorithm. Uses stack as deeply as the
        longest possible path will be.
        """
        # Set start position
        if not pos:
            pos = Pos((0, 0))

        # Stackframe:
        # (pos, directions): The current positions and the directions that still need checking.
        stack = [(pos, self.random_directions())]

        while stack:
            # print(f"{stack=}")
            pos, directions = stack.pop()

            while directions:
                # Consume one direction
                d = directions.pop()

                # Can we go there?
                try:
                    np = self.step(pos, d)
                except ValueError:
                    continue

                if show:
                    show(self, red=pos, green=np)

                # Is the new position np unused?
                if self[np] == 0:
                    # Remove wall
                    self.make_passage(pos, d)
                    # If we still have directions to check, push current position back
                    if directions:
                        stack.append((pos, directions))
                    # In any case, add the new position (and all directions)
                    stack.append((np, self.random_directions()))
                    break  # while directions: -> continue with np

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
