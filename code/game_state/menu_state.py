import pygame

from random import randint
from .game_state import GameState
from common import FONT_30, FONT_24
from ui import Label, Button, MultiLineLabel
from window import Window


class MenuState(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__caption: Label = Label("Симулятор нелегального лесоруба", FONT_30, "#000000",
                                      (205, 205, 205, 127), bg_padding=pygame.Vector2(12, 3))

        # Кнопки
        self.__button_color: str = "#a0a0a09f"
        self.__button_hover_color: str = "#cdcdcd9f"
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
        # Панель с обучением
        self.show_tutorial_screen: bool = True
        tutorial_text: list[str] = [
            "Следите за температурой с помощью термометра!",
            "Также следите за временем, потому что рано утром и вечером холоднее!",
            "(-30 до 10:00 и после 19:00, и -40 с 00:00 до 6:00)",
            "",
            "Управление:",
            "   Ходьба - WASD",
            "   Инвентарь | Сундук - TAB",
            "   Двери | Кровать | Магазины | Продажа - E",
            "   Использовать предмет - ЛКМ",
            "   Чтобы срубить дерево находитесь в радиусе действия инструмента и наведя курсор",
            "   на дерево жмите ЛКМ"
        ]
        self.tutorial_surface: pygame.Surface = pygame.Surface((Window.SIZE[0] - 180, Window.SIZE[1] - 40), flags=pygame.SRCALPHA)
        self.tutorial_surface.fill("#000000cf")
        tutorial_lbl: MultiLineLabel = MultiLineLabel(tutorial_text, FONT_24, "#ffffff")
        tutorial_lbl.draw(self.tutorial_surface, (4, 4))

        # Задний фон меню
        bg_image_id: int = randint(0, 2)
        self.__background_image = pygame.image.load(f"../resources/textures/menu_bg_image_{bg_image_id}.png").convert_alpha()
        self.__background_image = pygame.transform.scale(self.__background_image, Window.SIZE)

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            if self.show_tutorial_screen:
                self.show_tutorial_screen = False
            else:
                Window.running = False
                return

        # Если панель с обучением активна, то не обновляет кнопки
        if self.show_tutorial_screen:
            return

        if self.__play_button.is_hovered():
            self.__play_button.texture.fill(self.__button_hover_color)
        else:
            self.__play_button.texture.fill(self.__button_color)
        if self.__play_button.is_active():
            self.game_state_manager.change_state(self.game_state_manager.PLAY_STATE)

        if self.__settings_button.is_hovered():
            self.__settings_button.texture.fill(self.__button_hover_color)
        else:
            self.__settings_button.texture.fill(self.__button_color)
        # if self.__settings_button.is_active():
        #     self.game_state_manager.change_state(self.game_state_manager.SETTING_STATE)

        if self.__quit_button.is_hovered():
            self.__quit_button.texture.fill(self.__button_hover_color)
        else:
            self.__quit_button.texture.fill(self.__button_color)
        if self.__quit_button.is_active():
            Window.running = False
            return

        if self.__editor_button.is_hovered():
            self.__editor_button.texture.fill("#cdcdcd7f")
        else:
            self.__editor_button.texture.fill(self.__button_color)
        if self.__editor_button.is_active():
            self.game_state_manager.change_state(self.game_state_manager.LEVEL_LIST)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.blit(self.__background_image, (0, 0))
        self.__caption.draw(Window.ui_surface, (-1, 90))

        self.__play_button.draw(Window.ui_surface)
        self.__settings_button.draw(Window.ui_surface)
        self.__quit_button.draw(Window.ui_surface)
        self.__editor_button.draw(Window.ui_surface)

        if self.show_tutorial_screen:
            Window.ui_surface.blit(
                self.tutorial_surface,
                (Window.SIZE[0] // 2 - self.tutorial_surface.width // 2, Window.SIZE[1] // 2 - self.tutorial_surface.height // 2)
            )
