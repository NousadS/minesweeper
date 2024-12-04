from abc import abstractmethod

import pygame


class State(pygame.sprite.Sprite):
    def __init__(self, instance: "Instance"):
        super().__init__()

        self.instance: "Instance" = instance
        self.textures: "Textures" = self.instance.textures
        self.screen: pygame.surface.Surface = self.instance.screen
        
        self.image = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def event(self, event: pygame.event.Event) -> None: ...
