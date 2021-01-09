#! /usr/bin/env python3

import sys
from typing import List, Dict, Tuple, Optional, NewType
from random import shuffle, randrange, choice, randint
from time import sleep

# import pygame

Pos = NewType("Pos", Tuple[int, int])
Direction = NewType("Direction", str)

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (200, 50, 50)
# GREEN = (50, 200, 50)
# LIGHT_BLUE = (230, 230, 255)
#
# # Einige Werte zum Malen
# size: int = 100
# line_width: int = 5
#
# surface: pygame.surface.Surface
#
#
#
# def wait(self) -> None:
#     # self.keywait()
#     pygame.display.flip()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     sleep(0.05)
#
#
# def keywait(self) -> None:
#     pygame.display.flip()
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#                 return
#         sleep(0.05)
#
#
# def show_init(self) -> None:
#     pygame.init()
#
#     self.surface = pygame.display.set_mode(
#         (self.size * self.width + 2, self.size * self.height + 2)
#     )
#     self.surface.fill(WHITE)
#     pygame.display.flip()
#
#     return
#
#
# # NW  N  NE
# #   W   E
# # SW  S  SE
#
# def square(
#         self, pos: Pos, red: Optional[Pos] = None, green: Optional[Pos] = None
# ) -> None:
#     xpos, ypos = pos[0], pos[1]
#     el = self.grid[ypos][xpos]
#
#     nw = (xpos * self.size, ypos * self.size)
#     ne = ((xpos + 1) * self.size, (ypos) * self.size)
#     sw = (xpos * self.size, (ypos + 1) * self.size)
#     se = ((xpos + 1) * self.size, (ypos + 1) * self.size)
#
#     color = LIGHT_BLUE
#     if el == 0:
#         color = BLACK
#     if red and pos == red:
#         color = RED
#     if green and pos == green:
#         color = GREEN
#     pygame.draw.rect(self.surface, color, nw + (self.size, self.size))
#
#     # North Border
#     if not (el & 1):
#         pygame.draw.line(self.surface, BLACK, nw, ne, width=self.line_width)
#
#     # East Border
#     if not (el & 2):
#         pygame.draw.line(self.surface, BLACK, ne, se, width=self.line_width)
#
#     # South Border
#     if not (el & 4):
#         pygame.draw.line(self.surface, BLACK, sw, se, width=self.line_width)
#
#     # West Border
#     if not (el & 8):
#         pygame.draw.line(self.surface, BLACK, nw, sw, width=self.line_width)
#
#
# def show(self, red: Optional[Pos] = None, green: Optional[Pos] = None):
#     for y in range(0, self.height):
#         for x in range(0, self.width):
#             self.square(Pos((x, y)), red, green)
#
#     self.wait()


class Labyrinth:
    """ Store a labyrinth as a List of Lists of Integers.

    Passages exist in the 4 cardinal directions, N, E, S, and W. We store them
    as bit flags (N=1, E=2, S=4, W=8). When set, a passage exists from the current
    cell into the direction indicated by the bitflag.
    """

    # Grid size
    width: int
    height: int
    grid: List[List[int]]

    # Einige Konstanten
    directions: Dict[Direction, int] = {
        Direction("N"): 1,
        Direction("E"): 2,
        Direction("S"): 4,
        Direction("W"): 8,
    }

    opposite: Dict[Direction, Direction] = {
        Direction("N"): Direction("S"),
        Direction("S"): Direction("N"),
        Direction("W"): Direction("E"),
        Direction("E"): Direction("W")
    }

    dx: Dict[Direction, int] = {
        Direction("N"): 0,
        Direction("S"): 0,
        Direction("E"): 1,
        Direction("W"): -1
    }
    dy: Dict[Direction, int] = {
        Direction("N"): -1,
        Direction("S"): 1,
        Direction("E"): 0,
        Direction("W"): 0
    }

    def __init__(self, width: int = 10, height: int = 10) -> None:
        """ Construct a labyrinth with no passages in the given dimensions """
        # Remeber labyrinth dimensions
        self.width = width
        self.height = height

        # Create empty labyrinth
        # Rows
        self.grid = [[]] * self.height

        # Columns with 0's
        for y in range(0, self.height):
            self.grid[y] = [0] * self.width

        return

    def __repr__(self) -> str:
        """ Dump the current labyrinths passages as raw integer values """
        s = ""

        for y in range(0, self.height):
            s += f"{y=}: "
            for x in range(0, self.width):
                s += f"{self.grid[y][x]:04b} "
            s += "\n"

        return s

    def __getitem__(self, item: Pos) -> int:
        """ Return the passages at position item: Pos from the labyrinth """
        r = self.grid[item[1]][item[0]]
        return r

    def __setitem__(self, key: Pos, value: int) -> None:
        """ Set the passages at position key: Pos to value: int """
        self.grid[key[1]][key[0]] = value
        return

    def position_valid(self, p: Pos) -> bool:
        """ Predicate, returns true if the position p: Pos is valid for this labyrinth """
        if 0 <= p[0] < self.width and 0 <= p[1] < self.height:
            return True
        else:
            return False

    def direction_valid(self, d: Direction) -> bool:
        """ Predicate, returns true if the Direction d is valid """
        directions = list(self.directions.keys())
        if d not in directions:
            return False
        else:
            return True

    def step(self, p: Pos, d: Direction) -> Pos:
        """ Starting at Pos p, walk one step into Direction d, return a new position.

        Raise ValueError if the Direction is invalid.
        Raise ValueError if the initial position is invalid.

        Raise ValueError if the step would lead off the grid.

        The new position is guaranteed to be valid.
        """
        if not self.direction_valid(d):
            raise ValueError(f"Invalid Direction {d=}")

        if not self.position_valid(p):
            raise ValueError(f"Invalid Position {p=}")

        np = Pos((p[0] + self.dx[d], p[1] + self.dy[d]))
        if not self.position_valid(np):
            raise ValueError(f"Invalid Position {np=}: Step from {p=} into {d=} leaves the grid.")

        return np

    def make_passage(self, p: Pos, d: Direction) -> None:
        """ At Pos p, make a passage into Direction d, also add the reverse passage.

        Raise ValueError if the Direction is invalid.
        Raise ValueError if the Pos is invalid.
        Raise ValueError if the Passage would lead off the grid.
        """
        if not self.direction_valid(d):
            raise ValueError(f"Invalid Direction {d=}")

        if not self.position_valid(p):
            raise ValueError(f"Invalid Position {p=}")

        np = self.step(p, d)
        self[p] |= self.directions[d]
        self[np] |= self.directions[self.opposite[d]]

        return


    def carve(self, pos: Optional[Pos] = None) -> None:
        """ carve passages starting at Pos p using recursive backtracking.

        Carves passages into the labyrinth, starting at Pos p (Default: 0,0),
        using a recursive backtracking algorithm. Uses stack as deeply as the
        longest possible path will be.
        """
        # Set start position
        if not pos:
            pos = Pos((0, 0))

        # probe in random order
        directions = list(self.directions.keys())
        shuffle(directions)
        for d in directions:
            # try to step into this direction
            try:
                np = self.step(pos, d)
            except ValueError as e:
                # We stepped off the grid
                continue

            # if the position is clean, make a passage, and recurse
            if self[np] == 0:
                self.make_passage(pos, d)
                self.carve(np)

    def carve_more(self, walls_to_remove: int = 0):
        """ Remove walls_to_remove more walls, randomly.

        After applying carve(), we randomly delete walls_to_remove many more walls
        to create for multiple valid pathes to the goal.

        We guarantee that each new passage is actually a wall removed, and that
        new passages do not lead off the grid.
        """
        to_go = walls_to_remove
        while to_go:
            # Choose a random position and direction
            pos = Pos((randrange(self.width), randrange(self.height)))
            directions = list(self.directions.keys())
            d = choice(directions)

            # and check if deleting the wall would change things.
            elem = self[pos]
            new_elem = elem | self.directions[d]
            if elem != new_elem:
                # Also check if the passage would lead off the grid
                try:
                    newpos = self.step(pos, d)
                except ValueError as e:
                    continue

                # The new passage will keep us on grid and change things
                self.make_passage(pos, d)
                to_go -= 1  # one done


if __name__ == "__main__":
    labyrinth = Labyrinth()
    labyrinth.carve()
    print(labyrinth)

    more = randint(5, 10)
    labyrinth.carve_more(more)
    print(labyrinth)
