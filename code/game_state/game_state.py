import pygame


class GameState:
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        self.game_state_manager = game_state_manager

    def update(self, *args, **kwargs) -> None:
        ...

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        ...
