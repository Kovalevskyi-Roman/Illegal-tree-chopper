import json
import pygame

from common import TILE_SIZE


class TileManager:
    tiles: tuple[str, ...] = tuple()
    tile_textures: tuple[pygame.Surface, ...] = tuple()

    @classmethod
    def init(cls) -> None:
        cls.load_tiles()
        cls.scale_textures_to((TILE_SIZE, TILE_SIZE))

    @classmethod
    def load_tiles(cls) -> None:
        try:
            with open("../resources/data/tiles.json", "r") as file:
                cls.tiles = tuple(json.load(file))

            tiles: list[pygame.Surface] = list()
            for tile in cls.tiles:
                tile_texture = pygame.image.load(f"../resources/textures/tiles/{tile}").convert_alpha()
                tiles.append(tile_texture)

            cls.tile_textures = tuple(tiles)

        except FileNotFoundError:
            print("ERROR: File 'tiles.json' not found.")

    @classmethod
    def scale_textures_by(cls, factor: float | int) -> None:
        tiles: list[pygame.Surface] = list()
        for tile in cls.tile_textures:
            tiles.append(pygame.transform.scale_by(tile, factor))

        cls.tile_textures = tuple(tiles)

    @classmethod
    def scale_textures_to(cls, size: pygame.typing.SequenceLike[int | float]) -> None:
        tiles: list[pygame.Surface] = list()
        for tile in cls.tile_textures:
            tiles.append(pygame.transform.scale(tile, size))

        cls.tile_textures = tuple(tiles)
