import pygame
import json

from game_state import GameState
from ui import MultiLineEntry
from window import Window
from common import FONT_18


class DataEditor(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)

        self.entry: MultiLineEntry = MultiLineEntry(
            pygame.Rect((0, 0), Window.SIZE),
            pygame.Surface(Window.SIZE),
            FONT_18,
            "#dddddd"
        )
        self.entry.texture.fill("#323232")
        self.entry.active = True

        self.editor = None

    def init(self) -> None:
        self.editor = self.game_state_manager.GAME_STATES.get(self.game_state_manager.EDITOR)
        self.entry.set_text(json.dumps(self.editor.game_objects[self.editor.selected_game_object], indent=4))
        pygame.key.start_text_input()

    def update(self, *args, **kwargs) -> None:
        self.entry.update()

        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.editor.game_objects[self.editor.selected_game_object] = json.loads(self.entry.get_as_one_line())
            self.game_state_manager.change_state(self.game_state_manager.EDITOR)
            pygame.key.stop_text_input()

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.entry.draw(Window.ui_surface)
