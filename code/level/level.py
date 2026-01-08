import pygame

from .tile_map import TileMap


class Level:
    def __init__(self, file_name: str) -> None:
        self.tile_map: TileMap = TileMap(file_name)

    def draw(self, surface: pygame.Surface) -> None:
        self.tile_map.draw(surface)

    def update(self) -> None:
        ...
