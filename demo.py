#! /usr/bin/env python 3

from random import randrange

from src.labyrinth import Labyrinth, Pos
from src.sidewinder import Sidewinder
from src.binarytree import BinaryTree
from src.backtracking import Backtracking
from src.depthfirst import DepthFirst
from src.labyrinth_painter import LabyrinthPainter


def show_and_wait(lab: Labyrinth, red: Pos, green: Pos):
    painter.show(lab, red, green)
    LabyrinthPainter.wait()

for c in [BinaryTree, Sidewinder, Backtracking, DepthFirst]:
    labyrinth = Labyrinth(carver=c, width=20, height=20)
    painter = LabyrinthPainter(labyrinth, size=30, line_width=4)
    labyrinth.carve(show=show_and_wait)

    while True:
        red = Pos((randrange(0, 20), randrange(0, 20)))
        green = Pos((randrange(0, 20), randrange(0, 20)))
        if red != green:
            break
    print(f"carver: {c} {red=} {green=}")
    painter.show(labyrinth, red=red, green=green)
    LabyrinthPainter.keywait()
