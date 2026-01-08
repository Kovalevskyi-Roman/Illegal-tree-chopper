import json
import pygame

from .tile_manager import TileManager


class TileMap:
    def __init__(self, file_name: str) -> None:
        self.tiles: tuple[tuple[int, ...]] | None = None
        self.load(file_name)

    def load(self, file_name: str) -> None:
        with open(f"../resources/data/levels/{file_name}.json") as file:
            tiles: list[tuple[int, ...]] = list()
            for layer in json.load(file).get("tile_map"):
                tiles.append(tuple(layer))

            self.tiles = tuple(tiles)

    def draw(self, surface: pygame.Surface) -> None:
        for row in range(len(self.tiles)):
            for column in range(len(self.tiles[row])):
                surface.blit(
                    TileManager.tile_textures[self.tiles[row][column]],
                             (column * TileManager.tile_size, row * TileManager.tile_size)
                )

