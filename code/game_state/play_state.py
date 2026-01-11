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
        self.level_manager.update_level()

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.level_manager.draw_level(surface)
