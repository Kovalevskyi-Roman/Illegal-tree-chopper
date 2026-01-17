import pygame

from typing import Any
from window import Window
from common import GAME_OBJECT_SIZE
from inventory import Inventory
from .character import Character


class Chest(Character):
    def __init__(self):
        super().__init__()

        self.rect.width = GAME_OBJECT_SIZE
        self.rect.height = GAME_OBJECT_SIZE

        self.inventory: Inventory = Inventory()
        self.inventory.max_length = 100

        self.inventory_opened: bool = False
        self.texture = pygame.image.load("../resources/textures/game_objects/chest.png").convert_alpha()
        self.texture = pygame.transform.scale(self.texture, self.rect.size)

    def from_game_object(self, game_object: dict[str, Any]) -> None:
        self.rect.topleft = game_object.get("data").get("position")
        self.inventory.items = game_object.get("data").get("items")

    def to_game_object(self) -> dict[str, Any]:
        return {
            "name": "chest",
            "data": {
                "position": self.rect.topleft,
                "items": self.inventory.items,
            }
        }

    def update(self, *args, **kwargs) -> None:
        player = kwargs.get("player")
        if not player.inventory_opened:
            self.inventory_opened = False
            return

        if not self.rect.colliderect(player.rect):
            self.inventory_opened = False
            return

        self.inventory_opened = True
        self.inventory.update([274, 32])

        if player.inventory.selected_item != -1:
            selected_item = player.inventory.items[player.inventory.selected_item]
            self.inventory.add_item(
                selected_item.get("item"),
                selected_item.get("count")
            )
            player.inventory.remove_item(selected_item.get("item"), selected_item.get("count"))
            player.inventory.selected_item = -1
            player.inventory.hovered_item = -1

        elif self.inventory.selected_item != -1:
            selected_item = self.inventory.items[self.inventory.selected_item]
            player.inventory.add_item(
                selected_item.get("item"),
                selected_item.get("count")
            )
            self.inventory.remove_item(selected_item.get("item"), selected_item.get("count"))
            self.inventory.selected_item = -1
            self.inventory.hovered_item = -1

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        surface.blit(self.texture, self.rect.topleft - offset)

        if self.inventory_opened:
            self.inventory.draw(Window.ui_surface, [274, 32])
            self.inventory.draw_item_data(Window.ui_surface, [16, 16])
