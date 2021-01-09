#! /usr/bin/env python 3

from random import randint

from src.backtracking import Backtracking
from src.labyrinth_painter import LabyrinthPainter

labyrinth = Backtracking()
painter = LabyrinthPainter(labyrinth)

labyrinth.carve()
painter.show(labyrinth)
print(labyrinth)

more = randint(5, 10)
labyrinth.carve_more(more)
painter.show(labyrinth)
print(labyrinth)
LabyrinthPainter.keywait()