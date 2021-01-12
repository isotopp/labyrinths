from typing import List, Dict, Tuple, Optional, NewType
from random import shuffle, randrange, choice, randint

Pos = NewType("Pos", Tuple[int, int])
Direction = NewType("Direction", str)


class Labyrinth:
    """Store a labyrinth as a List of Lists of Integers.

    Passages exist in the 4 cardinal directions, N, E, S, and W. We store them
    as bit flags (N=1, E=2, S=4, W=8). When set, a passage exists from the current
    cell into the direction indicated by the bitflag.
    """

    # Grid size
    width: int
    height: int
    grid: List[List[int]]

    # Einige Konstanten
    _directions: Dict[Direction, int] = {
        Direction("N"): 1,
        Direction("E"): 2,
        Direction("S"): 4,
        Direction("W"): 8,
    }

    opposite: Dict[Direction, Direction] = {
        Direction("N"): Direction("S"),
        Direction("S"): Direction("N"),
        Direction("W"): Direction("E"),
        Direction("E"): Direction("W"),
    }

    dx: Dict[Direction, int] = {
        Direction("N"): 0,
        Direction("S"): 0,
        Direction("E"): 1,
        Direction("W"): -1,
    }
    dy: Dict[Direction, int] = {
        Direction("N"): -1,
        Direction("S"): 1,
        Direction("E"): 0,
        Direction("W"): 0,
    }

    def __init__(self, width: int = 10, height: int = 10) -> None:
        """ Construct a labyrinth with no passages in the given dimensions """
        self.width = width
        self.height = height
        self.grid = [[]] * self.height
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
        if not self.position_valid(item):
            raise ValueError(f"Invalid Position: {item=}")

        r = self.grid[item[1]][item[0]]
        return r

    def __setitem__(self, key: Pos, value: int) -> None:
        """ Set the passages at position key: Pos to value: int """
        if not self.position_valid(key):
            raise ValueError(f"Invalid Position: {key=}")

        if not (0<=value<=15):
            raise ValueError(f"Invalid cell value: {value=}")

        self.grid[key[1]][key[0]] = value
        return

    def position_valid(self, p: Pos) -> bool:
        """ Predicate, returns true if the position p: Pos is valid for this labyrinth """
        return 0 <= p[0] < self.width and 0 <= p[1] < self.height

    def direction_valid(self, d: Direction) -> bool:
        """ Predicate, returns true if the Direction d is valid """
        return d in self.directions()

    def directions(self) -> List[Direction]:
        return list(self._directions.keys())

    def random_directions(self) -> List[Direction]:
        """Return all cardinal directions in random order. """
        d = self.directions()
        shuffle(d)

        return d

    def step(self, p: Pos, d: Direction) -> Pos:
        """Starting at Pos p, walk one step into Direction d, return a new position.

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
            raise ValueError(
                f"Invalid Position {np=}: Step from {p=} into {d=} leaves the grid."
            )

        return np

    def can_make_passage(self, p: Pos, d: Direction) -> bool:
        """Predicate, true if making a passage at Pos p into Direction d would be valid, and change things."""
        if not self.direction_valid(d):
            raise ValueError(f"Invalid Direction: {d=}")

        if not self.position_valid(p):
            raise ValueError(f"Invalid Position: {p=}")

        try:
            np = self.step(p, d)
        except ValueError as e:
            # We stepped off the grid.
            return False

        # Success, if the world would change by removing this wall.
        pre_elem = self[p]
        post_elem = pre_elem | self._directions[d]
        return pre_elem != post_elem

    def make_passage(self, p: Pos, d: Direction) -> None:
        """At Pos p, make a passage into Direction d, also add the reverse passage.

        Raise ValueError if the Direction is invalid.
        Raise ValueError if the Pos is invalid.
        Raise ValueError if the Passage would lead off the grid.
        """
        if not self.direction_valid(d):
            raise ValueError(f"Invalid Direction {d=}")

        if not self.position_valid(p):
            raise ValueError(f"Invalid Position {p=}")

        np = self.step(p, d)
        self[p] |= self._directions[d]
        self[np] |= self._directions[self.opposite[d]]

        return

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
