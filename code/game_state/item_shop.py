import pygame

from character import Player
from .game_state import GameState


class ItemShop(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)

        self.__player: Player | None = None

    def update(self, *args, **kwargs) -> None:
        if self.__player is None:
            self.__player = self.game_state_manager.GAME_STATES.get(self.game_state_manager.PLAY_STATE).player

        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game_state_manager.change_state(self.game_state_manager.PLAY_STATE)
