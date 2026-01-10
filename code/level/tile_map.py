import json
import pygame

from window import Window
from .tile_manager import TileManager


class TileMap:
    def __init__(self, file_name: str) -> None:
        self.tiles: tuple[tuple[int, ...]] | None = None
        self.load(file_name)

    def load(self, file_name: str) -> None:
        with open(f"../resources/data/levels/{file_name}.json", "r") as file:
            tiles: list[tuple[int, ...]] = list()
            for layer in json.load(file).get("tile_map"):
                tiles.append(tuple(layer))

            self.tiles = tuple(tiles)

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        for row in range(len(self.tiles)):
            if row * TileManager.TILE_SIZE - offset.y > Window.SIZE[1]:
                break
            if row * TileManager.TILE_SIZE - offset.y < -TileManager.TILE_SIZE:
                continue

            for column in range(len(self.tiles[row])):
                tile_texture = TileManager.tile_textures[self.tiles[row][column]]
                tile_position = pygame.Vector2(column * TileManager.TILE_SIZE,row * TileManager.TILE_SIZE)

                if tile_position.x - offset.x > Window.SIZE[0]:
                    break
                if tile_position.x - offset.x < -TileManager.TILE_SIZE:
                    continue

                surface.blit(tile_texture, tile_position - offset)
