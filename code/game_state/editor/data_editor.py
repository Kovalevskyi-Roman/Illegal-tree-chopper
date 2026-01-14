import pygame

from game_state import GameState
from ui import Entry
from window import Window


class DataEditor(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)

        self.entry: Entry = Entry(
            pygame.Rect(10, 10, 500, 500),
            pygame.Surface((500, 500)),
            pygame.font.SysFont("Tahoma", 20),
            "#cdcdcd"
        )

    def update(self, *args, **kwargs) -> None:
        self.entry.update()

        if self.entry.active:
            self.entry.texture.fill("#434343")
        else:
            self.entry.texture.fill("#323232")

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.entry.draw(Window.ui_surface)
