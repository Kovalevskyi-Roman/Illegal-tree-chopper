import pygame

from .game_state import GameState


class MenuState(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.game_state_manager.change_state(self.game_state_manager.PLAY_STATE)
