#! /usr/bin/env python3

from typing import List, Dict
from random import shuffle
import turtle
from time import sleep


class Labyrinth:
    width: int
    height: int
    grid: List[List[int]]

    directions: Dict[str, int] = {"N": 1, "E": 2, "S": 4, "W": 8}
    opposite: Dict[str, str] = {"N": "S", "S": "N", "W": "E", "E": "W"}

    dx: Dict[str, int] = {"N": 0, "S": 0, "E": 1, "W": -1}
    dy: Dict[str, int] = {"N": -1, "S": 1, "E": 0, "W": 0}

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

        return

    def carve_from(self, x=0, y=0) -> None:
        # Mögliche Schritte mischen
        directions = list(self.directions.keys())
        shuffle(directions)

        # Rundum durchprobieren
        for d in directions:
            # neues Feld berechnen
            nx, ny = x + self.dx[d], y + self.dy[d]

            # Wenn das neue Feld gültige Koordinaten hat:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                # Wenn das neue Feld leer ist:
                if self.grid[ny][nx] == 0:
                    # Altes Feld: Mauer in die neue Richtung einreissen
                    self.grid[y][x] |= self.directions[d]
                    # Neues Feld: Mauer aus der neuen Richtung einreissen
                    self.grid[ny][nx] |= self.directions[self.opposite[d]]

                    # Weiter marschieren
                    self.carve_from(nx, ny)

    def show_init(self) -> turtle.Turtle:
        s = turtle.getscreen()
        t = turtle.Turtle()
        t.penup()
        t.goto(-150, 150)
        t.pendown()

        return t

    def square(self, t: turtle.Turtle, corners: int) -> None:
        t.speed(0)
        t.seth(0)

        t.pendown()
        for i in range(0,4):
            p = 2**i
            t.pencolor("black")
            if corners & p:
                t.pencolor("white")

            t.forward(30)
            t.right(90)

        t.penup()
        t.forward(30)

    def show(self):
        t = self.show_init()

        for y in range(0, self.height):
            for x in range(0, self.width):
                el = self.grid[y][x]
                self.square(t, el)
            t.seth(180)
            t.forward(30 * self.width)
            t.seth(270)
            t.forward(30)

        sleep(10)


if __name__ == "__main__":
    grid = Labyrinth()
    grid.carve_from()
    print(grid)
    grid.show()
