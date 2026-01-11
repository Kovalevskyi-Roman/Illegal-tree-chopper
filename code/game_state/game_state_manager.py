import pygame

from . import GameState
from .menu_state import MenuState
from .play_state import PlayState


class GameStateManager:
    MENU_STATE = MenuState
    PLAY_STATE = PlayState

    def __init__(self) -> None:
        self.GAME_STATES: dict[type, GameState] = {
            self.MENU_STATE: MenuState(self),
            self.PLAY_STATE: PlayState(self)
        }

        self.current_state = self.MENU_STATE

    def change_state(self, state: type[GameState]) -> None:
        if state not in self.GAME_STATES.keys():
            return

        self.current_state = state

    def update(self, *args, **kwargs) -> None:
        self.GAME_STATES.get(self.current_state).update(*args, **kwargs)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.GAME_STATES.get(self.current_state).draw(surface, *args, **kwargs)
