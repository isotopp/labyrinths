import sys
from time import sleep
from typing import Optional
import pygame

from src.labyrinth import Labyrinth, Pos

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
LIGHT_BLUE = (230, 230, 255)


class LabyrinthPainter:
    surface: pygame.surface.Surface

    # Einige Werte zum Malen
    size: int
    line_width: int

    def __init__(self, lab, size=100, line_width=5) -> None:
        self.size = size
        self.line_width = line_width

        self.show_init(lab)

        return

    @staticmethod
    def wait() -> None:
        # self.keywait()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        sleep(0.05)

    @staticmethod
    def keywait() -> None:
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            sleep(0.05)

    def show_init(self, lab: Labyrinth) -> None:
        pygame.init()

        self.surface = pygame.display.set_mode(
            (
                self.size * lab.width + self.line_width,
                self.size * lab.height + self.line_width,
            )
        )
        self.surface.fill(WHITE)
        pygame.display.flip()

        return

    # NW  N  NE
    #   W   E
    # SW  S  SE

    def square(
        self,
        lab: Labyrinth,
        pos: Pos,
        red: Optional[Pos] = None,
        green: Optional[Pos] = None,
    ) -> None:
        xpos, ypos = pos[0], pos[1]
        el = lab[pos]

        nw = (xpos * self.size, ypos * self.size)
        ne = ((xpos + 1) * self.size, ypos * self.size)
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

    def show(
        self, lab: Labyrinth, red: Optional[Pos] = None, green: Optional[Pos] = None
    ):
        for y in range(0, lab.height):
            for x in range(0, lab.width):
                self.square(lab, Pos((x, y)), red, green)
