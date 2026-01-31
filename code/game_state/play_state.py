import pygame
import common

from .game_state import GameState
from window import Window
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

        # Обновление игрового времени
        common.game_time += Window.DELTA
        if common.game_time >= 24 * 60:
            common.game_time = 0
            common.survived_days_count += 1

        # Обновляет текущий уровень
        self.level_manager.update_level()
        current_level = self.level_manager.get_current_level()

        # Обновляет все игровые объекты на текущем уровне
        GameObject.update_objects(
            current_level.game_objects,
            player=self.player,
            camera=self.camera,
            level_manager=self.level_manager,
            characters=current_level.characters,
            game_state_manager=self.game_state_manager
        )
        # Удаляет все игровые объекты у которых health <= 0
        current_level.game_objects = list(
            filter(lambda o: o.get("data").get("health", 1) > 0, current_level.game_objects)
        )

        # Обновляет предметы если инвентарь открыт
        if self.player.inventory_opened:
            Item.update_items(player=self.player, level=current_level)

        # Если игрок умер
        if self.player.health <= 0:
            self.game_state_manager.change_state(self.game_state_manager.DEATH_SCREEN_STATE)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.fill("#202030")  # Закрашивает задний фон
        self.level_manager.draw_level(surface)
