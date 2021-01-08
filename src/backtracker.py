#! /usr/bin/env python3

from typing import List, Dict
from random import shuffle

class Labyrinth:
    width: int
    height: int
    l: List[List[int]]

    directions: Dict[str, int] = {"N": 1, "S": 2, "E": 4, "W": 8}
    opposite: Dict[str, str] = {"N": "S", "S": "N", "W": "E", "E": "W"}

    dx: Dict[str, int] = {"N": 0, "S": 0, "E": 1, "W": -1}
    dy: Dict[str, int] = {"N": -1, "S": 1, "E": 0, "W": 0}

    def __str__(self) -> str:
        s = ""

        # # Als Zahlen drucken
        # for y in range(0, self.height):
        #     s += f"{y=} "
        #     for x in range(0, self.width):
        #         s += f"{self.l[y][x]} "
        #     s += "\n"
        # s += "\n"

        # Als Labyrinth drucken
        # Zeilen
        s += "--" + "-" * (self.width * 2 + 1) + "\n"
        for y in range(0, self.height):
            s += f"{y}|"

            # Spalten
            for x in range(0, self.width):
                el = self.l[y][x]  # aktuelles Feld auslesen

                # Haben wir einen Durchgang nach Süden offen? Dann " "
                s += " " if el & self.directions["S"] else "-"

                # Haben wir einen Durchgang nach Osten offen (oder von Osten kommend?)
                if el & self.directions["E"]:
                    check = el | self.l[y][x+1]
                    s += " " if check & self.directions["S"] else "-"
                else:
                    s += "|"
            s += "\n"
        s += "--" + "-" * (self.width * 2 + 1) + "\n"
        return s

    def __init__(self, width:int =10, height:int =10) -> None:
        # Merken der Labyrinthgroesse
        self.width = width
        self.height = height

        # leeres Labyrinth

        # Zeilen erzeugen
        self.l = [[]] * self.height

        # Spalten erzeugen und mit 0 vorbelegen
        for y in range(0, self.height):
            self.l[y] = [0] * self.width

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
                if self.l[ny][nx] == 0:
                    # Altes Feld: Mauer in die neue Richtung einreissen
                    self.l[y][x] |= self.directions[d]
                    # Neues Feld: Mauer aus der neuen Richtung einreissen
                    self.l[ny][nx] |= self.directions[self.opposite[d]]

                    # Weiter marschieren
                    self.carve_from(nx, ny)


if __name__ == "__main__":
    l = Labyrinth()
    l.carve_from()
    print(l)
