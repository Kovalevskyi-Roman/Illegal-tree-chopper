from typing import Any

import pygame

from game_state import GameState
from level import TileMap, Level, TileManager
from object import GameObject
from window import Window


class Editor(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)
        self.level_name: str = ""
        self.tile_map: TileMap | None = None
        self.game_objects: list[dict[str, Any]] = list()

        self.offset: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.scroll_speed: int = 5

        self.selected_tile: int = 0

    def init(self, level_name: str):
        self.level_name = level_name
        self.tile_map = TileMap(self.level_name)
        self.game_objects = Level.load_game_objects(self.level_name)
        self.offset = pygame.math.Vector2(0, 0)

    def update(self, *args, **kwargs) -> None:
        key = pygame.key.get_pressed()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_pressed = pygame.mouse.get_pressed()

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

        scroll = tuple(filter(lambda e: e.type == pygame.MOUSEWHEEL, Window.events))
        if scroll:
            self.selected_tile -= scroll[0].y

            if self.selected_tile < 0:
                self.selected_tile = len(TileManager.tiles) - 1
            elif self.selected_tile > len(TileManager.tiles) - 1:
                self.selected_tile = 0

        if mouse_pressed[0]:
            mouse_tile_pos = ((mouse_pos + self.offset) // TileManager.TILE_SIZE)

            if mouse_tile_pos.y < 0 or mouse_tile_pos.x < 0:
                return

            while mouse_tile_pos.y > len(self.tile_map.tiles) - 1:
                self.tile_map.tiles.append(list())

            while mouse_tile_pos.x > len(self.tile_map.tiles[int(mouse_tile_pos.y)]) - 1:
                self.tile_map.tiles[int(mouse_tile_pos.y)].append(self.selected_tile)

            self.tile_map.tiles[int(mouse_tile_pos.y)][int(mouse_tile_pos.x)] = self.selected_tile

        elif mouse_pressed[2]:
            mouse_tile_pos = ((mouse_pos + self.offset) // TileManager.TILE_SIZE)

            if mouse_tile_pos.y < 0 or mouse_tile_pos.x < 0 or mouse_tile_pos.y > len(self.tile_map.tiles) - 1:
                return

            if mouse_tile_pos.x > len(self.tile_map.tiles[int(mouse_tile_pos.y)]) - 1:
                return

            self.tile_map.tiles[int(mouse_tile_pos.y)][int(mouse_tile_pos.x)] = -1

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.tile_map.draw(surface, self.offset)

        for game_object in self.game_objects:
            GameObject.draw(surface, game_object, self.offset)
