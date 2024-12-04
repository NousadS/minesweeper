import pathlib

import pygame

from .states import Game, Menu, State
from .textures import Textures


class Instance:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((600, 620), pygame.SRCALPHA)
        pygame.display.set_caption("MineSweeper")

        self.textures: Textures = Textures(
            pathlib.Path().cwd() / "data" / "textures.png"
        )

        self.clock = pygame.time.Clock()

        self.objects = pygame.sprite.Group()

        self.background: State = Game(
            self,
            iwidth=10,
            iheight=10,
            mines=0,
        )
        self.foreground: State = Menu(self)

        while self.background is not None:
            self.screen.fill((203, 219, 252))

            if len(self.objects) < 2:
                if self.background is not None:
                    self.objects.add(self.background)

                if self.foreground is not None:
                    self.objects.add(self.foreground)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.background = None

                print(len(self.objects) != 1)

                if len(self.objects) != 1:
                    self.foreground.event(event)
                else:
                    self.background.event(event)

            self.objects.update()
            self.objects.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(60)
