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
