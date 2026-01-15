import pygame

from .game_state import GameState
from camera import Camera
from character import Player
from level import LevelManager


class PlayState(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.player = Player()
        self.camera = Camera(self.player)
        self.level_manager = LevelManager(self.player, self.camera)

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.game_state_manager.change_state(self.game_state_manager.MENU_STATE)

        self.level_manager.update_level()

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.fill("#0c0c1e")
        self.level_manager.draw_level(surface)
