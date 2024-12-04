from typing import Generator

import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(
        self,
        game: "Game",
        textures: "Textures",
        x: int,
        y: int,
        ix: int,
        iy: int,
        width: int,
        height: int,
    ) -> None:
        super().__init__()

        self.game: "Game" = game
        self.textures: "Textures" = textures

        self.x: int = x
        self.y: int = y

        self.ix: int = ix
        self.iy: int = iy

        self.width: int = width
        self.height: int = height

        self.mine: bool = False
        self.number: int = 0

        self.opened: bool = False
        self.flagged: bool = False
        self.hovered: bool = False

        self.image = pygame.Surface([self.width, self.height])

        self.rect = self.image.get_rect()
        self.rect.x = self.ix * self.width + self.x
        self.rect.y = self.iy * self.height + self.y

    @property
    def neighbors(self) -> Generator["Cell", None, None]:
        for dy, dx in [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]:
            ix, iy = self.ix + dx, self.iy + dy

            if 0 <= ix < self.game.iwidth and 0 <= iy < self.game.iheight:
                yield self.game.get(ix, iy)

    def update(self):
        self.image.fill((203, 219, 252))

        match (self.hovered, self.opened, self.flagged, self.mine):
            case (False, False, _, _):
                self.blit(self.textures.BUTTON)

            case (False, True, True, _):
                self.blit(self.textures.BUTTON_DISABLED)
            case (False, True, False, False):
                self.blit(self.textures.BUTTON_DISABLED)
            case (False, True, False, True):
                self.blit(self.textures.RED_BUTTON_DISABLED)

            case (True, False, _, _):
                self.blit(self.textures.BUTTON_HOVER)

            case (True, True, True, _):
                self.blit(self.textures.BUTTON_DISABLED_HOVER)
            case (True, True, False, False):
                self.blit(self.textures.BUTTON_DISABLED_HOVER)
            case (True, True, False, True):
                self.blit(self.textures.RED_BUTTON_DISABLED_HOVER)

        match (self.opened, self.flagged, self.mine):
            case (True, True, True):
                self.blit(self.textures.MISC_MINE)
                self.blit(self.textures.WHITER)
                self.blit(self.textures.MISC_FLAG)
            case (True, True, False):
                self.blit(self.textures.MISC_FLAG)
                self.blit(self.textures.MISC_CROSS)
            case (True, False, True):
                self.blit(self.textures.MISC_MINE)
                self.blit(self.textures.MISC_CROSS)
            case (True, False, False):
                self.blit(getattr(self.textures, f"NUMBER_{self.number}"))
            case (False, True, _):
                self.blit(self.textures.MISC_FLAG)

    def event(self, event: pygame.event.Event):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP and self.hovered:
            if not self.game.generated:
                self.game.generate([self.ix, self.iy])

            if event.button == 1 and not self.flagged and not self.opened:
                self.open()
            elif event.button == 3 and not self.opened:
                self.flagged = not self.flagged

    def blit(self, texture: pygame.surface.Surface):
        self.image.blit(
            pygame.transform.scale(
                texture,
                (self.width, self.height),
            ),
            (0, 0),
        )

    def open(self):
        if not self.opened:
            self.opened = True

            if self.number == 0:
                for neighbor in self.neighbors:
                    if not neighbor.opened:
                        neighbor.open()
