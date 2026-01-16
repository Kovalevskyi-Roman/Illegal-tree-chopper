import pygame

from ui import Label, Button
from window import Window
from .game_state import GameState
from common import FONT_30, FONT_24


class MenuState(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__caption: Label = Label("Симулятор нелегального лесоруба", FONT_30, "#000000",
                                      (205, 205, 205, 127), bg_padding=pygame.Vector2(12, 3))

        self.__play_button: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(-1, 270, 300, 36),
            pygame.Surface((300, 36), flags=pygame.SRCALPHA),
            "Играть",
            FONT_24,
            "#000000"
        )

        self.__settings_button: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(-1, 320, 300, 36),
            pygame.Surface((300, 36), flags=pygame.SRCALPHA),
            "Настройки",
            FONT_24,
            "#000000"
        )

        self.__quit_button: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(-1, 370, 300, 36),
            pygame.Surface((300, 36), flags=pygame.SRCALPHA),
            "Выйти из игры",
            FONT_24,
            "#000000"
        )

        self.__editor_button: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(-1, 420, 300, 36),
            pygame.Surface((300, 36), flags=pygame.SRCALPHA),
            "Редактор уровней",
            FONT_24,
            "#000000"
        )

        self.__background_image = pygame.image.load("../resources/textures/menu_background.png").convert_alpha()
        self.__background_image = pygame.transform.scale(self.__background_image, Window.SIZE)

    def update(self, *args, **kwargs) -> None:
        if self.__play_button.is_hovered():
            self.__play_button.texture.fill("#cdcdcd7f")
        else:
            self.__play_button.texture.fill("#a0a0a07f")
        if self.__play_button.is_active():
            self.game_state_manager.change_state(self.game_state_manager.PLAY_STATE)

        if self.__settings_button.is_hovered():
            self.__settings_button.texture.fill("#cdcdcd7f")
        else:
            self.__settings_button.texture.fill("#a0a0a07f")
        # if self.__settings_button.is_active():
        #     self.game_state_manager.change_state(self.game_state_manager.SETTING_STATE)

        if self.__quit_button.is_hovered():
            self.__quit_button.texture.fill("#cdcdcd7f")
        else:
            self.__quit_button.texture.fill("#a0a0a07f")
        if self.__quit_button.is_active() or pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            Window.running = False
            return

        if self.__editor_button.is_hovered():
            self.__editor_button.texture.fill("#cdcdcd7f")
        else:
            self.__editor_button.texture.fill("#a0a0a07f")
        if self.__editor_button.is_active():
            self.game_state_manager.change_state(self.game_state_manager.LEVEL_LIST)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.blit(self.__background_image, (0, 0))
        self.__caption.draw(Window.ui_surface, (-1, 90))

        self.__play_button.draw(Window.ui_surface)
        self.__settings_button.draw(Window.ui_surface)
        self.__quit_button.draw(Window.ui_surface)
        self.__editor_button.draw(Window.ui_surface)
