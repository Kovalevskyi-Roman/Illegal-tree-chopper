import pygame
import common

from .game_state import GameState
from character import Player
from item import Item
from ui import Label
from window import Window


class ItemShop(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)

        self.__width: int = 250
        self.__height: int = 120

        self.__caption: Label = Label("Магазин Предметов", common.FONT_24, "#ffffff")
        self.__player: Player | None = None

        self.hovered_item: int = -1
        self.skip_items: int = 3

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game_state_manager.change_state(self.game_state_manager.PLAY_STATE)

        if self.__player is None:
            self.__player = self.game_state_manager.GAME_STATES.get(self.game_state_manager.PLAY_STATE).player

        self.hovered_item = -1
        item_rect = pygame.Rect(8, self.__caption.render.height + 16, self.__width, self.__height)
        for i in range(self.skip_items, len(Item.items)):
            item = Item.items[i]
            # Покупка предмета
            if pygame.mouse.get_just_pressed()[0] and item_rect.collidepoint(pygame.mouse.get_pos()) and \
                    common.player_money >= item.get("price"):
                self.__player.inventory.add_one_item(i)
                common.player_money -= item.get("price")
                break

            elif item_rect.collidepoint(pygame.mouse.get_pos()):
                self.hovered_item = i
                break

            item_rect.x += self.__width + 8
            if item_rect.right > Window.SIZE[0]:
                item_rect.x = 8
                item_rect.y += self.__height + 8

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__caption.draw(Window.ui_surface, [-1, 8])
        Window.ui_surface.blit(
            common.FONT_24.render(f"Деньги: {common.player_money}$", True, "#ffffff"),
            [8, 8]
        )

        x = 8
        y = self.__caption.render.height + 16
        for i in range(self.skip_items, len(Item.items)):
            item = Item.items[i]
            bg_color = (127, 127, 127)

            if i == self.hovered_item:
                bg_color = (200, 200, 200)

            pygame.draw.rect(Window.ui_surface, bg_color, [x, y, self.__width, self.__height])
            Window.ui_surface.blit(item.get("texture"), [x + self.__width / 2 - common.ITEM_SIZE / 2, y + 4])
            Window.ui_surface.blit(
                common.FONT_18.render(item.get("name"), True, "#ffffff"),
                [x + 4, y + common.ITEM_SIZE + 4]
            )
            Window.ui_surface.blit(
                common.FONT_18.render(f"Цена: {item.get("price", 0)}$", True, "#ffffff"),
                [x + 4, y + common.ITEM_SIZE + common.FONT_18.get_height() + 4]
            )

            x += self.__width + 8
            if x + self.__width > Window.SIZE[0]:
                x = 8
                y += self.__height + 8
