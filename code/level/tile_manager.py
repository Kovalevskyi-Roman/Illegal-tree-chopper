import json
import pygame

from common import TILE_SIZE


class TileManager:
    tiles: tuple[str, ...] = tuple()
    tile_textures: tuple[pygame.Surface, ...] | None = None

    @classmethod
    def init(cls) -> None:
        cls.load_tiles()
        cls.scale_to_tile_textures((TILE_SIZE, TILE_SIZE))

    @classmethod
    def load_tiles(cls) -> None:
        cls.tile_textures = None
        tiles: list[pygame.Surface] = list()

        with open("../resources/data/tiles.json", "r") as file:
            cls.tiles = tuple(json.load(file))
            for tile in cls.tiles:
                tile_texture = pygame.image.load(f"../resources/textures/tiles/{tile}").convert_alpha()
                tiles.append(tile_texture)

        cls.tile_textures = tuple(tiles)

    @classmethod
    def scale_by_tile_textures(cls, factor: float | int) -> None:
        if cls.tile_textures is None:
            raise ValueError("Tile textures not loaded!")

        tiles: list[pygame.Surface] = list()
        for tile in cls.tile_textures:
            tiles.append(pygame.transform.scale_by(tile, factor))

        cls.tile_textures = tuple(tiles)

    @classmethod
    def scale_to_tile_textures(cls, size: pygame.typing.SequenceLike[int | float]) -> None:
        if cls.tile_textures is None:
            raise ValueError("Tile textures not loaded!")

        tiles: list[pygame.Surface] = list()
        for tile in cls.tile_textures:
            tiles.append(pygame.transform.scale(tile, size))

        cls.tile_textures = tuple(tiles)
