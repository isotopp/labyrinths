#! /usr/bin/env python3

from typing import List, Optional

class Labyrinth:
    width: int = 10
    height: int = 0
    l: List[List[int]] = None
    dir: List[List[int]] = None

    def __str__(self):
        s= ""

        for i in self.l:
            for j in i:
                 s += f"{j} "
            s += "\n"

        return s

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height

        self.l = [[0] * width] *height

        self.dir = {
            "N": {"x": 0, "y": -1 },
            "S": {"x": 0, "y": +1},
            "E": {"x": -1, "y": 0},
            "W": {"x": +1, "y": -},
        }

        return

    def carve_from(self, x=0, y=0):
        directions = ["N", "E", "S", "W"]
        shuffle(directions)

        for d in directions:


if __name__ == "__main__":
    l = Labyrinth()
    l.carve_from()
    print(l)
