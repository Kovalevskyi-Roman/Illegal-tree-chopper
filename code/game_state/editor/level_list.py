import pygame

from pathlib import Path
from game_state import GameState
from ui import Button


class LevelList(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.font_24 = pygame.font.SysFont("Tahoma", 24)

        self.levels: list[str] = self.load_levels()
        self.level_buttons: list[Button] = self.create_level_buttons()

    def load_levels(self) -> list[str]:
        levels: list[str] = list()
        path: Path = Path("../resources/data/levels/")

        for path in path.iterdir():
            if not path.is_file():
                continue

            if path.suffix == ".json":
                levels.append(path.stem)

        return levels

    def create_level_buttons(self) -> list[Button]:
        buttons: list[Button] = list()

        for i in range(len(self.levels)):
            buttons.append(Button(
                pygame.mouse.get_just_pressed,
                0,
                pygame.Rect(-1, 10 + i * 42, 400, 32),
                pygame.Surface((400, 32), flags=pygame.SRCALPHA),
                self.levels[i],
                self.font_24,
                "#000000"
            ))
            buttons[i].texture.fill("#a0a0a07f")

        return buttons

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game_state_manager.change_state(self.game_state_manager.MENU_STATE)

        for i in range(len(self.level_buttons)):
            button = self.level_buttons[i]

            if button.is_hovered():
                button.texture.fill("#cdcdcd7f")
            else:
                button.texture.fill("#a0a0a07f")

            if button.is_active():
                self.game_state_manager.GAME_STATES.get(
                    self.game_state_manager.EDITOR
                ).init(self.levels[i])
                self.game_state_manager.change_state(self.game_state_manager.EDITOR)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        for button in self.level_buttons:
            button.draw(surface)
