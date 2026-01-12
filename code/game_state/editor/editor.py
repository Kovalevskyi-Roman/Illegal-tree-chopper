from typing import Any

import pygame

from game_state import GameState
from level import TileMap, Level
from object import GameObject


class Editor(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)
        self.level_name: str = ""
        self.tile_map: TileMap | None = None
        self.game_objects: list[dict[str, Any]] = list()
        self.offset: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.scroll_speed: int = 5

    def init(self, level_name: str):
        self.level_name = level_name
        self.tile_map = TileMap(self.level_name)
        self.game_objects = Level.load_game_objects(self.level_name)
        self.offset = pygame.math.Vector2(0, 0)

    def update(self, *args, **kwargs) -> None:
        key = pygame.key.get_pressed()

        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game_state_manager.change_state(self.game_state_manager.LEVEL_LIST)

        if key[pygame.K_d]:
            self.offset.x += self.scroll_speed
        elif key[pygame.K_a]:
            self.offset.x -= self.scroll_speed
        if key[pygame.K_w]:
            self.offset.y -= self.scroll_speed
        elif key[pygame.K_s]:
            self.offset.y += self.scroll_speed

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.tile_map.draw(surface, self.offset)

        for game_object in self.game_objects:
            GameObject.draw(surface, game_object, self.offset)
