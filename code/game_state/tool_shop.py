import pygame
import common

from character import Player
from tool import Tool
from ui import Label, MultiLineLabel
from window import Window
from .game_state import GameState


class ToolShop(GameState):
    def __init__(self, game_state_manager: "GameStateManager", *args, **kwargs):
        super().__init__(game_state_manager, *args, **kwargs)

        self.surface: pygame.Surface = pygame.Surface(Window.SIZE, flags=pygame.SRCALPHA)
        self.caption: Label = Label("Магазин Инструментов", common.FONT_24, "#ffffff")

        self.__player: Player | None = None
        self.width: int = 180
        self.height: int = 200

        self.hovered_tool: int = 0

    def update_surface(self) -> None:
        x = 8
        y = self.caption.render.height + 16
        for i in range(len(Tool.tools)):
            tool = Tool.tools[i]
            color = (127, 127, 127, 127)

            if i == self.hovered_tool:
                color = (200, 200, 200, 127)

            if i == self.__player.tool:
                color = (127, 255, 127, 127)
            pygame.draw.rect(self.surface, color, [x, y, self.width, self.height])
            self.surface.blit(tool.get("texture"), [x, y])
            self.surface.blit(
                common.FONT_18.render(f"{tool.get("price")}$", True, "#ffffff"),
                [x + self.width - common.FONT_18.size(f"{tool.get("price")}$")[0] - 4, y + 4]
            )
            MultiLineLabel(
                [tool.get("name"), f"Урон: {tool.get("damage")}", f"Радиус: {tool.get("range")}", f"Перезарядка: {tool.get("cool_down")}"],
                common.FONT_18,
                "#ffffff"
            ).draw(self.surface, [x + 4, y + tool.get("texture").height + 4])

            x += self.width + 8
            if x + self.width > Window.SIZE[0]:
                x = 8
                y += self.height + 8

    def update(self, *args, **kwargs) -> None:
        if self.__player is None:
            self.__player = self.game_state_manager.GAME_STATES.get(self.game_state_manager.PLAY_STATE).player

        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game_state_manager.change_state(self.game_state_manager.PLAY_STATE)

        if self.hovered_tool != -1:
            self.update_surface()

        self.hovered_tool = -1
        tool_rect = pygame.Rect(8, self.caption.render.height + 16, self.width, self.height)
        for i in range(len(Tool.tools)):
            tool = Tool.tools[i]

            if pygame.mouse.get_just_pressed()[0] and tool_rect.collidepoint(pygame.mouse.get_pos()) and \
                    common.player_money >= tool.get("price"):
                common.player_money -= tool.get("price")
                tool["price"] = 0
                self.__player.tool = i
                break

            elif tool_rect.collidepoint(pygame.mouse.get_pos()):
                self.hovered_tool = i
                break

            tool_rect.x += self.width + 8
            if tool_rect.right > Window.SIZE[0]:
                tool_rect.x = 8
                tool_rect.y += self.height + 8

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        if self.__player is None:
            return

        self.caption.draw(Window.ui_surface, [-1, 8])
        Window.ui_surface.blit(
            common.FONT_24.render(f"Деньги: {common.player_money}$", True, "#ffffff"),
            [8, 8]
        )

        Window.ui_surface.blit(self.surface, [0, 0])
