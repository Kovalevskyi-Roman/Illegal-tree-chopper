import pygame

from camera import Camera
from character import Player
from .tile_map import TileMap


class Level:
    def __init__(self, file_name: str, player: Player, camera: Camera, level_manager: "LevelManager") -> None:
        self.tile_map: TileMap = TileMap(file_name)

        self.player = player
        self.camera = camera
        self.level_manager = level_manager

    def draw(self, surface: pygame.Surface) -> None:
        self.tile_map.draw(surface, self.camera.offset)
        self.player.draw(surface, self.camera.offset)

    def update(self) -> None:
        self.player.update()
        self.camera.update()

        if self.player.rect.x > 300:
            self.level_manager.current_level = "aboba"
        else:
            self.level_manager.current_level = "test"
