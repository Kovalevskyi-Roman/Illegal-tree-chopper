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

        self.file_name = file_name
        self.player = player
        self.camera = camera
        self.level_manager = level_manager

    @classmethod
    def load_game_objects(cls, file_name: str) -> list[dict[str, Any]]:
        with open(f"../resources/data/levels/{file_name}.json", "r") as file:
            return json.load(file).get("game_objects")

    def save_level(self) -> None:
        content: dict | None = None
        with open(f"../resources/data/levels/{self.file_name}.json", "r") as file:
            content = json.load(file)

        content["game_objects"] = self.game_objects
        with open(f"../resources/data/levels/{self.file_name}.json", "w") as file:
            json.dump(content, file, indent=4)

    def draw(self, surface: pygame.Surface) -> None:
        self.tile_map.draw(surface, self.camera.offset)
        self.player.draw(surface, self.camera.offset)

        for game_object in self.game_objects:
            GameObject.draw(surface, game_object, self.camera.offset)

    def update(self) -> None:
        self.player.update(self.game_objects, self.camera.offset)
        # border
        if self.player.rect.x < 0:
            self.player.rect.x = 0
        if self.player.rect.y < 0:
            self.player.rect.y = 0

        if self.player.rect.right > self.tile_map.width:
            self.player.rect.right = self.tile_map.width
        if self.player.rect.bottom > self.tile_map.height:
            self.player.rect.bottom = self.tile_map.height

        self.camera.update()

        for game_object in self.game_objects:
            GameObject.update(game_object, player=self.player, camera=self.camera, level_manager=self.level_manager)

        self.game_objects = list(filter(lambda o: o.get("data").get("health", 1) > 0, self.game_objects))
