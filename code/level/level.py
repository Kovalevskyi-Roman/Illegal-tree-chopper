import json
import random
import pygame
import common

from typing import Any
from camera import Camera
from character import Player, Character
from game_object import GameObject
from item import Item
from window import Window
from .tile_map import TileMap


class Level:
    def __init__(self, file_name: str, player: Player, camera: Camera, level_manager: "LevelManager") -> None:
        self.file_name = file_name
        self.player = player
        self.camera = camera
        self.level_manager = level_manager

        self.tile_map: TileMap | None = None
        self.game_objects: list[dict[str, Any]] = list()
        self.characters: list[Character] = list()
        self.temperature_range: list[int] = list()
        self.temperature: int = 0
        self.temperature_update_timer: float = 0
        self.colder_at_night: bool = False

        self.load_level()

    @classmethod
    def load_game_objects(cls, file_name: str) -> list[dict[str, Any]]:
        with open(f"../resources/data/levels/{file_name}.json", "r") as file:
            return json.load(file).get("game_objects")

    def load_level(self) -> None:
        self.tile_map: TileMap = TileMap(self.file_name)
        self.game_objects: list[dict[str, Any]] = self.load_game_objects(self.file_name)

        with open(f"../resources/data/levels/{self.file_name}.json", "r") as file:
            content = json.load(file)

            self.temperature_range = content.get("temperature_range")
            self.colder_at_night = content.get("colder_at_night")
            self.temperature = random.randint(*self.temperature_range)

    def save_level(self) -> None:
        content: dict | None = None
        with open(f"../resources/data/levels/{self.file_name}.json", "r") as file:
            content = json.load(file)

        content["temperature_range"] = self.temperature_range
        content["game_objects"] = self.game_objects
        with open(f"../resources/data/levels/{self.file_name}.json", "w") as file:
            json.dump(content, file, indent=4)

    def draw(self, surface: pygame.Surface) -> None:
        self.tile_map.draw(surface, self.camera.offset)
        self.player.draw(surface, self.camera.offset)

        for character in self.characters:
            character.draw(surface, self.camera.offset)

        for game_object in self.game_objects:
            GameObject.draw(surface, game_object, self.camera.offset)

    def update(self) -> None:
        self.temperature_update_timer -= Window.DELTA
        if self.temperature_update_timer <= 0:
            self.temperature = random.randint(*self.temperature_range)
            self.temperature_update_timer = 30

        self.player.update(self.game_objects, self.camera.offset, self.temperature, self.colder_at_night)

        if self.player.inventory.selected_item != -1:
            if Item.can_use(self.player.inventory.get_selected_item().get("item")):
                Item.use(self.player.inventory.get_selected_item().get("item"), player=self.player, game_objects=self.game_objects)
                self.player.inventory.remove_by_index(self.player.inventory.selected_item)

        for character in self.characters:
            character.update(player=self.player)

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