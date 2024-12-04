import pygame

import pendulum

from ..game import Game
from ..state import State


class Menu(State):
    def __init__(
        self,
        *args,
        result: int = None,
        time: pendulum.DateTime = None,
        **kwargs,
    ) -> None:
        super().__init__(*args)

        self.width: int = 8
        self.height: int = 8

        self.mines: int = 20

        self.play: bool = False

        self.result = result
        self.time = time

    def update(self) -> None:
        self.image.fill((255, 255, 255, 172))

        if self.play:
            self.instance.background.kill()
            self.instance.background = Game(
                self.instance,
                iwidth=self.width,
                iheight=self.height,
                mines=self.mines,
            )

            self.instance.foreground.kill()
            self.instance.foreground = None

        font_30 = pygame.font.SysFont("Fira Sans Bold", 30)
        font_60 = pygame.font.SysFont("Fira Sans Bold", 60)

        if self.result is None:
            texts = [
                [font_60.render("MINESWEEPER", True, (0, 0, 0)), 200],
                [font_30.render("by Nousad", True, (0, 0, 0)), 240],
                [font_30.render("Size: {}x{}".format(self.width, self.height), True, (0, 0, 0)), 340],
                [font_30.render("Mines: {}".format(self.mines), True, (0, 0, 0)), 365],
            ]
        else:
            texts = [
                [font_60.render("MINESWEEPER", True, (0, 0, 0)), 200],
                [font_30.render("by Nousad", True, (0, 0, 0)), 240],
                [font_60.render("{}".format("You win!" if self.result == 1 else "You lose..."), True, (0, 0, 0)), 320],
                [font_30.render("Size: {}x{}".format(self.width, self.height), True, (0, 0, 0)), 390],
                [font_30.render("Mines: {}".format(self.mines), True, (0, 0, 0)), 415],
            ]

        for text in texts:
            self.image.blit(text[0], ((self.image.get_width() - text[0].get_width()) // 2, text[1]))
                
    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.width += 1
                self.height = self.width
            if event.key == pygame.K_s:
                self.width -= 1

                if self.width <= 1:
                    self.width = 2

                self.height = self.width

            if event.key == pygame.K_d:
                self.mines += 1
            if event.key == pygame.K_a:
                self.mines -= 1

            if event.key == pygame.K_e:
                self.mines = int((self.width * self.height) * (40 / (16 * 16)))
            # if event.key == pygame.K_q:
            #     self.width = int(self.mines * ((16 * 16) / 40))
            #     self.height = self.width

            if self.mines self.mines = self.width

            if event.key == pygame.K_SPACE:
                self.play = True
