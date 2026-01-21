import json

import pygame

from pathlib import Path
from game_state import GameState
from ui import Button, Entry
from window import Window


class LevelList(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.font_24 = pygame.font.SysFont("Tahoma", 24)

        self.levels: list[str] = self.load_levels()
        self.level_buttons: list[Button] = self.create_level_buttons()

        self.new_level_entry: Entry = Entry(
            pygame.Rect(830, 10, 400, 30),
            pygame.Surface((400, 30), flags=pygame.SRCALPHA),
            self.font_24,
            "#000000"
        )
        self.new_level_btn: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(1240, 10, 30, 30),
            pygame.Surface((30, 30), flags=pygame.SRCALPHA),
            "+",
            self.font_24,
            "#000000"
        )

    @classmethod
    def load_levels(cls) -> list[str]:
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

        y = 10
        x = 10
        for level in self.levels:
            buttons.append(Button(
                pygame.mouse.get_just_pressed,
                0,
                pygame.Rect(x, y, 400, 30),
                pygame.Surface((400, 30), flags=pygame.SRCALPHA),
                level,
                self.font_24,
                "#000000"
            ))
            buttons[-1].texture.fill("#a0a0a07f")

            y += 40
            if y + 30 >= Window.SIZE[1]:
                y = 10
                x = 420

        return buttons

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            pygame.key.stop_text_input()
            self.new_level_entry.active = False
            self.game_state_manager.change_state(self.game_state_manager.MENU_STATE)

        self.new_level_entry.update()
        if self.new_level_entry.active:
            self.new_level_entry.texture.fill("#cdcdcd7f")
        else:
            self.new_level_entry.texture.fill("#a0a0a07f")

        if self.new_level_btn.is_hovered():
            self.new_level_btn.texture.fill("#cdcdcd7f")
        else:
            self.new_level_btn.texture.fill("#a0a0a07f")
        if self.new_level_btn.is_active():
            with open(f"../resources/data/levels/{self.new_level_entry.get_text()}.json", "w") as file:
                json.dump({"tile_map": [[]], "game_objects": []}, file, indent=4)

            self.levels = self.load_levels()
            self.level_buttons = self.create_level_buttons()
            self.new_level_entry.text.clear()
            self.new_level_entry.cursor_pos = -1
            self.new_level_entry.active = False

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
            button.draw(Window.ui_surface)

        self.new_level_entry.draw(Window.ui_surface)
        self.new_level_btn.draw(Window.ui_surface)
