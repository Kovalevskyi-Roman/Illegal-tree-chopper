import json
import pygame

from typing import Any
from random import randint
from .tile_map import TileMap
from camera import Camera
from character import Character, Player, character_factory
from game_object import GameObject
from window import Window


class Level:
    def __init__(self, file_name: str, player: Player, camera: Camera, level_manager: "LevelManager") -> None:
        self.file_name = file_name
        self.player = player
        self.camera = camera
        self.level_manager = level_manager

        self.tile_map: TileMap | None = None
        self.game_objects: list[dict[str, Any]] = list()
        self.characters: list[Character] = list()
        self.temperature_range: list[int] = list()  # [min, max]
        self.temperature: int = 0
        self.temperature_change_timer: float = 0
        self.colder_at_night: bool = False

        self.load_level()

    @classmethod
    def load_game_objects(cls, file_name: str) -> list[dict[str, Any]]:
        """Возвращает список всех игровых объектов на уровне 'file_name'."""
        with open(f"../resources/data/levels/{file_name}.json", "r") as file:
            return json.load(file).get("game_objects")

    def load_characters(self, content: dict[str, Any]) -> None:
        characters = content.get("characters", list())

        for character in characters:
            self.characters.append(character_factory(character))

    def load_level(self) -> None:
        self.tile_map = TileMap(self.file_name)
        self.game_objects = self.load_game_objects(self.file_name)

        with open(f"../resources/data/levels/{self.file_name}.json", "r") as file:
            content = json.load(file)

            self.load_characters(content)
            self.temperature_range = content.get("temperature_range", list([0, 0]))
            self.colder_at_night = content.get("colder_at_night")
            self.temperature = randint(self.temperature_range[0], self.temperature_range[1])

    def draw(self, surface: pygame.Surface) -> None:
        self.tile_map.draw(surface, self.camera.offset)
        self.player.draw(surface, self.camera.offset)

        for character in self.characters:
            character.draw(surface, self.camera.offset)

        for game_object in self.game_objects:
            GameObject.draw(surface, game_object, self.camera.offset)

    def update(self) -> None:
        # Обновляет температуру каждые 30 секунд
        self.temperature_change_timer -= Window.DELTA
        if self.temperature_change_timer <= 0:
            self.temperature = randint(*self.temperature_range)
            self.temperature_change_timer = 30

        self.player.update(self.game_objects, self.camera.offset,
                           self.temperature, self.colder_at_night, self.level_manager)

        for character in self.characters:
            character.update(player=self.player, level_manager=self.level_manager)

            if character.rect.x < 0:
                character.rect.x = 0
            if character.rect.y < 0:
                character.rect.y = 0
            if character.rect.right > self.tile_map.width:
                character.rect.right = self.tile_map.width
            if character.rect.bottom > self.tile_map.height:
                character.rect.bottom = self.tile_map.height

        # Границы уровня
        if self.player.rect.x < 0:
            self.player.rect.x = 0
        if self.player.rect.y < 0:
            self.player.rect.y = 0
        if self.player.rect.right > self.tile_map.width:
            self.player.rect.right = self.tile_map.width
        if self.player.rect.bottom > self.tile_map.height:
            self.player.rect.bottom = self.tile_map.height

        self.camera.update()
