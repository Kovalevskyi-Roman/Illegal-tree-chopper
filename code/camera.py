import pygame

from window import Window
from character import Character


class Camera:
    def __init__(self, target: Character) -> None:
        self.target = target
        self.offset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__smoothness: float = 0.025
        self.__box_size: float = 75

        self.set_offset()

    def set_offset(self, offset: pygame.Vector2 | None = None) -> None:
        if offset is None:
            self.offset.x += round(self.target.rect.centerx - (Window.SIZE[0] // 2) - self.offset.x)
            self.offset.y += round(self.target.rect.centery - (Window.SIZE[1] // 2) - self.offset.y)
            return

        self.offset = offset

    def update(self) -> None:
        distance: pygame.Vector2 = pygame.Vector2(
            round(self.target.rect.centerx - (Window.SIZE[0] // 2) - self.offset.x),
            round(self.target.rect.centery - (Window.SIZE[1] // 2) - self.offset.y)
        )

        self.offset += distance * self.__smoothness

        # if distance.length() > self.__box_size and self.target.direction:
        #     self.offset += distance * self.__smoothness
        #
        # elif not self.target.direction:
        #     self.offset += distance * self.__smoothness
