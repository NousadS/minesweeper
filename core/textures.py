import pathlib

import pygame


class Textures:
    class Identifiers:
        EMPTY = (0, 0)

        BUTTON = (0, 1)
        BUTTON_HOVER = (0, 2)
        BUTTON_DISABLED = (0, 3)
        BUTTON_DISABLED_HOVER = (0, 4)

        RED_BUTTON = (0, 5)
        RED_BUTTON_HOVER = (0, 6)
        RED_BUTTON_DISABLED = (0, 7)
        RED_BUTTON_DISABLED_HOVER = (0, 8)

        NUMBER_0 = (1, 0)
        NUMBER_1 = (1, 1)
        NUMBER_2 = (1, 2)
        NUMBER_3 = (1, 3)
        NUMBER_4 = (1, 4)
        NUMBER_5 = (1, 5)
        NUMBER_6 = (1, 6)
        NUMBER_7 = (1, 7)
        NUMBER_8 = (1, 8)
        NUMBER_9 = (1, 9)

        NUMBER_INFINITY = (0, 9)

        MISC_QUESTION = (2, 0)
        MISC_FLAG = (2, 1)
        MISC_MINE = (2, 2)
        MISC_CHECK = (2, 3)
        MISC_CROSS = (2, 4)
        MISC_START = (2, 5)
        MISC_LIGHT = (2, 6)
        MISC_GEAR = (2, 7)

        FACE_BASE = (4, 0)
        FACE_HAPPY = (4, 1)
        FACE_OH = (4, 2)
        FACE_EZ = (4, 3)
        FACE_DEATH = (4, 4)

        WHITER = (9, 0)
        DARKER = (9, 1)

    def __init__(self, path: pathlib.Path):
        self.block_size = 40
        self.size = 10

        self.textures = pygame.transform.scale(
            pygame.image.load(path).convert_alpha(),
            (self.block_size * self.size, self.block_size * self.size),
        )

    def __getattr__(self, name: str):
        if hasattr(self.Identifiers, name):
            texture = getattr(self.Identifiers, name)
        else:
            texture = self.Identifiers.MISC_CROSS

        return self.textures.subsurface(
            texture[1] * self.block_size,
            texture[0] * self.block_size,
            self.block_size,
            self.block_size,
        )
