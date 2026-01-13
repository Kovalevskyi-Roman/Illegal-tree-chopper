import json
import pygame

from copy import deepcopy
from typing import Any
from game_state import GameState
from game_state.editor.side_panel import SidePanel
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
        self.scroll_speed: int = 10
        self.selected_tile: int = 0
        self.selected_game_object: int = -1
        self.safe_tile_deleting = True
        self.move_game_object: bool = False
        self.snap_to_grid: bool = True

        self.side_panel: SidePanel = SidePanel(game_state_manager, self)

    def init(self, level_name: str):
        self.level_name = level_name
        self.tile_map = TileMap(self.level_name)
        self.game_objects = Level.load_game_objects(self.level_name)
        self.offset = pygame.math.Vector2(0, 0)
        self.selected_tile: int = 0
        self.selected_game_object: int = -1
        self.safe_tile_deleting = True
        self.move_game_object: bool = False
        self.snap_to_grid: bool = True

    def save(self) -> None:
        with open(f"../resources/data/levels/{self.level_name}.json", "w") as file:
            json.dump(
                {"tile_map": self.tile_map.tiles, "game_objects": self.game_objects},
                file,
                indent=4)

        self.game_state_manager.GAME_STATES.get(self.game_state_manager.PLAY_STATE).level_manager.load_levels()
        print(f"Level '{self.level_name}.json' saved")

    def update(self, *args, **kwargs) -> None:
        key = pygame.key.get_pressed()
        key_just_press = pygame.key.get_just_pressed()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_pressed = pygame.mouse.get_pressed()

        if key_just_press[pygame.K_ESCAPE]:
            if self.selected_game_object != -1:
                self.selected_game_object = -1
            else:
                self.save()
                self.game_state_manager.change_state(self.game_state_manager.LEVEL_LIST)

        elif key_just_press[pygame.K_m]:
            self.move_game_object = not self.move_game_object

        elif key_just_press[pygame.K_g]:
            self.snap_to_grid = not self.snap_to_grid

        elif key_just_press[pygame.K_c] and self.selected_game_object != -1:
            self.game_objects.append(deepcopy(self.game_objects[self.selected_game_object]))
            self.move_game_object = True
            self.selected_game_object = len(self.game_objects) - 1

        elif (key_just_press[pygame.K_BACKSPACE] or key_just_press[pygame.K_DELETE]) and self.selected_game_object != -1:
            self.game_objects.pop(self.selected_game_object)
            self.selected_game_object = -1

        if key[pygame.K_LCTRL] and key_just_press[pygame.K_s]:
            self.save()

        if key[pygame.K_d]:
            self.offset.x += self.scroll_speed
        elif key[pygame.K_a]:
            self.offset.x -= self.scroll_speed
        if key[pygame.K_w]:
            self.offset.y -= self.scroll_speed
        elif key[pygame.K_s] and not key[pygame.K_LCTRL]:
            self.offset.y += self.scroll_speed

        if self.selected_game_object == -1:
            self.move_game_object = False

        if self.move_game_object:
            self.game_objects[self.selected_game_object]["data"]["position"] = list(
                mouse_pos + self.offset
            )

            if self.snap_to_grid:
                self.game_objects[self.selected_game_object]["data"]["position"] = list(
                    (mouse_pos + self.offset) // TileManager.TILE_SIZE * TileManager.TILE_SIZE
                )

        scroll = tuple(filter(lambda e: e.type == pygame.MOUSEWHEEL, Window.events))
        if scroll:
            self.selected_tile -= scroll[0].y

            if self.selected_tile < 0:
                self.selected_tile = len(TileManager.tiles) - 1
            elif self.selected_tile > len(TileManager.tiles) - 1:
                self.selected_tile = 0

        self.side_panel.update()

        if mouse_pressed[0] and mouse_pos.x < Window.SIZE[0] - self.side_panel.width:
            for i in range(len(self.game_objects)):
                game_object = self.game_objects[i]
                rect = pygame.Rect(game_object.get("data").get("position"), [TileManager.TILE_SIZE, TileManager.TILE_SIZE])
                rect.topleft -= self.offset

                if rect.collidepoint(mouse_pos):
                    self.selected_game_object = i
                    return

            self.selected_game_object = -1
            mouse_tile_pos = ((mouse_pos + self.offset) // TileManager.TILE_SIZE)

            if mouse_tile_pos.y < 0 or mouse_tile_pos.x < 0:
                return

            while mouse_tile_pos.y > len(self.tile_map.tiles) - 1:
                self.tile_map.tiles.append(list())

            while mouse_tile_pos.x > len(self.tile_map.tiles[int(mouse_tile_pos.y)]) - 1:
                self.tile_map.tiles[int(mouse_tile_pos.y)].append(self.selected_tile)

            self.tile_map.tiles[int(mouse_tile_pos.y)][int(mouse_tile_pos.x)] = self.selected_tile

        elif mouse_pressed[2] and mouse_pos.x < Window.SIZE[0] - self.side_panel.width:
            mouse_tile_pos = ((mouse_pos + self.offset) // TileManager.TILE_SIZE)

            if mouse_tile_pos.y < 0 or mouse_tile_pos.x < 0 or mouse_tile_pos.y > len(self.tile_map.tiles) - 1:
                return

            if mouse_tile_pos.x > len(self.tile_map.tiles[int(mouse_tile_pos.y)]) - 1:
                return

            if self.safe_tile_deleting:
                self.tile_map.tiles[int(mouse_tile_pos.y)][int(mouse_tile_pos.x)] = -1
            else:
                self.tile_map.tiles[int(mouse_tile_pos.y)].pop(int(mouse_tile_pos.x))

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.tile_map.draw(surface, self.offset)

        for game_object in self.game_objects:
            GameObject.draw(surface, game_object, self.offset)

        self.side_panel.draw()
