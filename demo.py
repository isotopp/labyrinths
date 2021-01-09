#! /usr/bin/env python 3

from random import randint

from src.backtracking import Backtracking, Pos
from src.labyrinth_painter import LabyrinthPainter


def show_and_wait(lab: Backtracking, red: Pos, green: Pos):
    painter .show(lab, red, green)
    LabyrinthPainter.keywait()


labyrinth = Backtracking()
painter = LabyrinthPainter(labyrinth)

labyrinth.carve(show=show_and_wait)
painter.show(labyrinth)
print(labyrinth)

more = randint(5, 10)
labyrinth.carve_more(more, show=show_and_wait)
painter.show(labyrinth)
print(labyrinth)
LabyrinthPainter.keywait()
