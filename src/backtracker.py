#! /usr/bin/env python3

import sys
from typing import List, Dict, Tuple, Optional, NewType
from random import shuffle, randrange, choice, randint
from time import sleep

import pygame

Pos = NewType('Pos', Tuple[int, int])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
LIGHT_BLUE = (230, 230, 255)


class Labyrinth:
    # Grid size
    width: int
    height: int
    grid: List[List[int]]

    # Einige Konstanten
    directions: Dict[str, int] = {"N": 1, "E": 2, "S": 4, "W": 8}
    opposite: Dict[str, str] = {"N": "S", "S": "N", "W": "E", "E": "W"}

    dx: Dict[str, int] = {"N": 0, "S": 0, "E": 1, "W": -1}
    dy: Dict[str, int] = {"N": -1, "S": 1, "E": 0, "W": 0}

    # Einige Werte zum Malen
    size: int = 100
    line_width: int = 5

    surface: pygame.surface.Surface

    def __str__(self) -> str:
        s = ""

        # Als Zahlen drucken
        for y in range(0, self.height):
            s += f"{y=} "
            for x in range(0, self.width):
                s += f"{self.grid[y][x]} "
            s += "\n"
        s += "\n"

        return s

    def __init__(self, width: int = 10, height: int = 10) -> None:
        # Merken der Labyrinthgroesse
        self.width = width
        self.height = height

        # leeres Labyrinth

        # Zeilen erzeugen
        self.grid = [[]] * self.height

        # Spalten erzeugen und mit 0 vorbelegen
        for y in range(0, self.height):
            self.grid[y] = [0] * self.width

        self.show_init()
        return

    def wait(self) -> None:
        # self.keywait()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        sleep(0.05)

    def keywait(self) -> None:
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            sleep(0.05)

    def show_init(self) -> None:
        pygame.init()

        self.surface = pygame.display.set_mode(
            (self.size * self.width + 2, self.size * self.height + 2)
        )
        self.surface.fill(WHITE)
        pygame.display.flip()

        return

    # NW  N  NE
    #   W   E
    # SW  S  SE

    def square(
        self, pos: Pos, red: Optional[Pos] = None, green: Optional[Pos] = None
    ) -> None:
        xpos, ypos = pos[0], pos[1]
        el = self.grid[ypos][xpos]

        nw = (xpos * self.size, ypos * self.size)
        ne = ((xpos + 1) * self.size, (ypos) * self.size)
        sw = (xpos * self.size, (ypos + 1) * self.size)
        se = ((xpos + 1) * self.size, (ypos + 1) * self.size)

        color = LIGHT_BLUE
        if el == 0:
            color = BLACK
        if red and pos == red:
            color = RED
        if green and pos == green:
            color = GREEN
        pygame.draw.rect(self.surface, color, nw + (self.size, self.size))

        # North Border
        if not (el & 1):
            pygame.draw.line(self.surface, BLACK, nw, ne, width=self.line_width)

        # East Border
        if not (el & 2):
            pygame.draw.line(self.surface, BLACK, ne, se, width=self.line_width)

        # South Border
        if not (el & 4):
            pygame.draw.line(self.surface, BLACK, sw, se, width=self.line_width)

        # West Border
        if not (el & 8):
            pygame.draw.line(self.surface, BLACK, nw, sw, width=self.line_width)

    def show(self, red: Optional[Pos] = None, green: Optional[Pos] = None):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.square(Pos((x, y)), red, green)

        self.wait()

    def is_in_grid(self, p: Pos) -> bool:
        x, y = p[0], p[1]
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def step(self, p: Pos, d: str) -> Pos:
        directions = list(self.directions.keys())
        if d not in directions:
            raise ValueError(f"Invalid Direction {d=}")

        if not self.is_in_grid(p):
            raise ValueError(f"Invalid Position {p=}")

        nx, ny = p[0] + self.dx[d], p[1] + self.dy[d]
        return Pos((nx, ny))

    def carve_from(self, p: Optional[Pos] = None) -> None:
        if not p:
            p = Pos((0,0))

        # Mögliche Schritte mischen
        directions = list(self.directions.keys())
        shuffle(directions)

        # Rundum durchprobieren
        for d in directions:
            # neues Feld berechnen
            np = self.step(p, d)
            self.show(red=p, green=np)

            # Wenn das neue Feld gültige Koordinaten hat:
            if self.is_in_grid(np):
                # Wenn das neue Feld leer ist:
                if self.grid[np[1]][np[0]] == 0:
                    # Altes Feld: Mauer in die neue Richtung einreissen
                    self.grid[p[1]][p[0]] |= self.directions[d]
                    # Neues Feld: Mauer aus der neuen Richtung einreissen
                    self.grid[np[1]][np[0]] |= self.directions[self.opposite[d]]

                    # Weiter marschieren
                    self.carve_from(np)

    def carve_more(self, walls_to_remove: int = 0):
        to_go = walls_to_remove
        while to_go:
            # Zufällige x,y Position
            p = Pos((randrange(self.width), randrange(self.height)))

            # Zufällige Richtung
            directions = list(self.directions.keys())
            d = choice(directions)

            # Element an dieser Position
            el = self.grid[p[1]][p[0]]

            # Testweise Mauer weg hauen
            nel = el | self.directions[d]
            print(f"{p=} {d=} {el=} {nel=}")

            if nel != el:  # da wäre eine Mauer zum wegmachen
                # Prüfe ob der neue Durchgang in ein valides Feld führt
                np = self.step(p, d)
                if self.is_in_grid(np):
                    self.show(red=p)  # vorher anzeigen, red
                    self.wait()

                    # tut er, wir machen das Loch
                    self.grid[p[1]][p[0]] |= self.directions[d]
                    self.grid[np[1]][np[0]] |= self.directions[self.opposite[d]]

                    self.show(green=p)  # nachher anzeigen, green
                    self.wait()

                    to_go -= 1  # Entsprechend runterzählen


if __name__ == "__main__":
    grid = Labyrinth()
    grid.carve_from()
    grid.show()
    grid.wait()

    more = randint(5, 10)
    grid.carve_more(more)
    grid.show()
    grid.keywait()
