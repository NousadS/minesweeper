from typing import Generator

import pendulum
import pygame

class Status(pygame.sprite.Sprite):
    def __init__(
        self,
        game: "Game",
        textures: "Textures",
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        super().__init__()

        self.game: "Game" = game
        self.textures: "Textures" = textures

        self.start: pendulum.DateTime = pendulum.now()
        self.end: pendulum.DateTime = pendulum.now()

        self.width = width
        self.height = height

        self.button: int = 0
        self.left: int = 0

        self.result: int = 0
        self.created: bool = False

        self.image = pygame.Surface([self.width, self.height])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.end = pendulum.now()
        self.left = self.game.iwidth * self.game.iheight - self.game.flagged

        self.image.fill((255, 0, 0))

        if self.result != 0 and not self.created:
            from ..menu import Menu
            
            self.created = True
            self.game.instance.foreground = Menu(self.game.instance, result=self.result, time=self.end - self.start)

    def event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button = event.button
        else:
            self.button = 0
