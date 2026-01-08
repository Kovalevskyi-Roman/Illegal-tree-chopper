import json
import pygame


class TileManager:
    TILE_SIZE: int = 32
    tile_textures: tuple[pygame.Surface, ...] | None = None

    @classmethod
    def init(cls) -> None:
        cls.load_tile_textures()
        cls.scale_to_tile_textures((cls.TILE_SIZE, cls.TILE_SIZE))

    @classmethod
    def load_tile_textures(cls) -> None:
        cls.tile_textures = None
        tiles: list[pygame.Surface] = list()

        with open("../resources/data/tiles.json", "r") as file:
            content: list[dict] = json.load(file)
            for tile in content:
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
