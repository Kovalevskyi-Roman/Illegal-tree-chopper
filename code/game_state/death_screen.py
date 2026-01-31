import pygame
import common
from character import Player

from .game_state import GameState
from ui import Label, MultiLineLabel, Button
from window import Window


class DeathScreenState(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)

        self.__caption: Label = Label("Вы погибли", common.FONT_30, "#ffffff")
        self.__info_text = [
            f"{common.survived_days_count}"
        ]
        self.__info_lbl: MultiLineLabel = MultiLineLabel(self.__info_text, common.FONT_20, "#ffffff")

        self.__quit_button: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(-1, 370, 300, 36),
            pygame.Surface((300, 36), flags=pygame.SRCALPHA),
            "Выйти из игры",
            common.FONT_24,
            "#000000"
        )

        self.__player: Player | None = None

    def update(self, *args, **kwargs) -> None:
        if self.__player is None:
            self.__player = self.game_state_manager.GAME_STATES.get(self.game_state_manager.PLAY_STATE).player

            self.__info_text = [
                f"Дней прожито: {common.survived_days_count}",
                f"Деревьев срублено: {self.__player.trees_chopped}",
                f"Деревьев посажено: {self.__player.trees_planted}"
            ]
            self.__info_lbl.update(self.__info_text)

        if self.__quit_button.is_hovered():
            self.__quit_button.texture.fill("#cdcdcd7f")
        else:
            self.__quit_button.texture.fill("#a0a0a07f")
        if self.__quit_button.is_active() or pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            Window.running = False
            return

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__caption.draw(Window.ui_surface, [-1, 30])
        self.__info_lbl.draw(Window.ui_surface, [-1, 130 + common.FONT_30.get_height()])
        self.__quit_button.draw(Window.ui_surface)