import json
import pygame

from window import Window
from .tile_manager import TileManager
from common import TILE_SIZE


class TileMap:
    def __init__(self, file_name: str) -> None:
        self.tiles: list[list[int]] | None = None
        self.load(file_name)

        self.height: int = len(self.tiles) * TILE_SIZE
        self.width: int = len(self.tiles[0]) * TILE_SIZE

    def load(self, file_name: str) -> None:
        with open(f"../resources/data/levels/{file_name}.json", "r") as file:
            self.tiles = json.load(file).get("tile_map")

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        for row in range(len(self.tiles)):
            if row * TILE_SIZE - offset.y > Window.SIZE[1]:
                break
            if row * TILE_SIZE - offset.y < -TILE_SIZE:
                continue

            for column in range(len(self.tiles[row])):
                if self.tiles[row][column] == -1:
                    continue
                tile_texture = TileManager.tile_textures[self.tiles[row][column]]
                tile_position = pygame.Vector2(column * TILE_SIZE, row * TILE_SIZE)

                if tile_position.x - offset.x > Window.SIZE[0]:
                    break
                if tile_position.x - offset.x < -TILE_SIZE:
                    continue

                surface.blit(tile_texture, tile_position - offset)
