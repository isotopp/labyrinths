#! /usr/bin/env python 3

from random import randrange

from src.depthfirst import DepthFirst, Pos
from src.labyrinth_painter import LabyrinthPainter


def show_and_wait(lab: DepthFirst, red: Pos, green: Pos):
    painter.show(lab, red, green)
    LabyrinthPainter.wait()


labyrinth = DepthFirst(width=20, height=20)
painter = LabyrinthPainter(labyrinth, size=30, line_width=4)

start = Pos((10,10))
labyrinth.carve(start, show=show_and_wait)
# painter.show(labyrinth)
# print(labyrinth)

# more = randint(5, 10)
# labyrinth.carve_more(more) #, show=show_and_wait)
while True:
    red = Pos((randrange(0, 20), randrange(0, 20)))
    green = Pos((randrange(0, 20), randrange(0, 20)))
    if red != green:
        break
print(f"{red=} {green=}")
painter.show(labyrinth, red=red, green=green)
# print(labyrinth)
LabyrinthPainter.keywait()
