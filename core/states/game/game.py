import random
from typing import Generator

import pendulum
import pygame
import pygame.locals

from ..state import State
from .cell import Cell
from .status import Status


class Game(State):
    def __init__(
        self,
        *args,
        iwidth: int = 0,
        iheight: int = 0,
        mines: int = 0,
        **kwargs,
    ) -> None:
        super().__init__(*args)

        self.iwidth: int = iwidth
        self.iheight: int = iheight
        self.mines: int = mines

        self.width: int = self.image.get_width() - 40
        self.height: int = self.width  # self.image.get_height() - 40

        self.cell_width: int = (self.width - self.iwidth) // self.iwidth
        self.cell_height: int = (self.height - self.iheight) // self.iheight

        self.x: int = (self.image.get_width() - self.cell_width * self.iwidth) // 2
        self.y: int = self.image.get_height() - self.cell_height * self.iheight - 5

        self.field: list[list[Cell]] | None = None

        self.field = [
            [
                Cell(
                    self,
                    self.textures,
                    self.x,
                    self.y,
                    x,
                    y,
                    self.cell_width,
                    self.cell_height,
                )
                for x in range(self.iwidth)
            ]
            for y in range(self.iheight)
        ]

        self.field_group: pygame.sprite.Group = pygame.sprite.Group(
            *[self.field[y][x] for y in range(self.iheight) for x in range(self.iwidth)]
        )

        self.status: Status = Status(
            self,
            self.textures,
            0,
            0,
            self.width,
            50,
        )

        self.opened: int = 0
        self.flagged: int = 0

        self.generated: bool = False

    def generate(self, must_null: list[int]) -> None:
        self.generated = True

        positions: list[list[int]] = []

        for i in range(self.mines):
            position: list[int] | None = None

            while (
                not position
                or position in positions
                or position in [[n.ix, n.iy] for n in self.get(*must_null).neighbors]
            ):
                position = [
                    random.randint(0, self.iwidth - 1),
                    random.randint(0, self.iheight - 1),
                ]

            positions.append(position)

        for position in positions:
            self.get(*position).mine = True

        for cell in self.cells:
            cell.number = sum([neighbor.mine for neighbor in cell.neighbors])

        for neighbor in self.get(*must_null).neighbors:
            neighbor.open()

    def get(self, x: int, y: int) -> Cell:
        return self.field[y][x]

    @property
    def cells(self) -> Generator[Cell, None, None]:
        for y in range(self.iheight):
            for x in range(self.iwidth):
                yield self.get(x, y)

    def update(self):
        self.image.fill((0, 0, 0, 0))

        self.opened = 0
        self.flagged = 0

        for cell in self.cells:
            if cell.opened:
                self.opened += 1

            if cell.flagged:
                self.flagged += 1

        self.field_group.update()
        self.field_group.draw(self.image)

        for cell in self.cells:
            if cell.mine and cell.opened:
                self.status.result = -1

        if (self.opened + self.flagged) == len(list(self.cells)):
            self.status.result = 1

        self.status.update()

        for cell in self.cells:
            cell.update()

    def event(self, event: pygame.event.Event) -> None:
        self.status.event(event)

        for cell in self.cells:
            cell.event(event)
