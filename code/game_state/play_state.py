import pygame

from .game_state import GameState
from camera import Camera
from character import Player
from level import LevelManager
from item import Item
from game_object import GameObject


class PlayState(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.player = Player()
        self.camera = Camera(self.player)
        self.level_manager = LevelManager(self.player, self.camera)

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            if self.player.inventory_opened:
                self.player.inventory_opened = False
            else:
                self.game_state_manager.change_state(self.game_state_manager.MENU_STATE)

        self.level_manager.update_level()
        GameObject.update_objects(
            self.level_manager.get_current_level().game_objects,
            player=self.player,
            camera=self.camera,
            level_manager=self.level_manager,
            characters=self.level_manager.get_current_level().characters,
            game_state_manager=self.game_state_manager
        )
        self.level_manager.get_current_level().game_objects = list(
            filter(lambda o: o.get("data").get("health", 1) > 0, self.level_manager.get_current_level().game_objects)
        )

        if self.player.inventory_opened:
            Item.update_items(player=self.player, level=self.level_manager.levels.get(self.level_manager.current_level))

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.fill("#0c0c1e")
        self.level_manager.draw_level(surface)
