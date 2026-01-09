import json
import pygame

from typing import Any
from camera import Camera
from character import Player
from object import GameObject
from .tile_map import TileMap


class Level:
    def __init__(self, file_name: str, player: Player, camera: Camera, level_manager: "LevelManager") -> None:
        self.tile_map: TileMap = TileMap(file_name)
        self.game_objects: list[dict[str, Any]] = self.load_game_objects(file_name)

        self.player = player
        self.camera = camera
        self.level_manager = level_manager

    def load_game_objects(self, file_name: str) -> list[dict[str, Any]]:
        with open(f"../resources/data/levels/{file_name}.json", "r") as file:
            return json.load(file).get("game_objects")

    def draw(self, surface: pygame.Surface) -> None:
        self.tile_map.draw(surface, self.camera.offset)
        self.player.draw(surface, self.camera.offset)

        for game_object in self.game_objects:
            GameObject.draw(surface, game_object, self.camera.offset)

    def update(self) -> None:
        self.player.update()
        self.camera.update()

        for game_object in self.game_objects:
            GameObject.update(game_object, player=self.player, level_manager=self.level_manager)
