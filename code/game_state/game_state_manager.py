import pygame

from .game_state import GameState
from .menu_state import MenuState
from .play_state import PlayState
from .tool_shop import ToolShop
from .item_shop import ItemShop
from .death_screen import DeathScreenState

from .editor import LevelList
from .editor import Editor
from .editor import DataEditor


class GameStateManager:
    # Чтобы избежать цикличного импорта все типы игровых состояний записаны как константы в этом классе.
    # Доступ к этому классу есть у каждого игрового состояния.
    MENU_STATE = MenuState
    PLAY_STATE = PlayState
    TOOL_SHOP_STATE = ToolShop
    ITEM_SHOP_STATE = ItemShop
    DEATH_SCREEN_STATE = DeathScreenState

    LEVEL_LIST = LevelList
    EDITOR = Editor
    DATA_EDITOR = DataEditor

    def __init__(self) -> None:
        self.GAME_STATES: dict[type, GameState] = {
            self.MENU_STATE: MenuState(self),
            self.PLAY_STATE: PlayState(self),
            self.TOOL_SHOP_STATE: ToolShop(self),
            self.ITEM_SHOP_STATE: ItemShop(self),
            self.DEATH_SCREEN_STATE: DeathScreenState(self),

            self.LEVEL_LIST: LevelList(self),
            self.EDITOR: Editor(self),
            self.DATA_EDITOR: DataEditor(self)
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
