import pygame

from typing import Any
from item import Item
from common import ITEM_SIZE, FONT_18


class Inventory:
    def __init__(self) -> None:
        # [{item: int, count: int}, ...]
        self.items: list[dict[str, int]] = list()
        self.max_stack_count: int = 999
        self.width: int = 4

        self.hovered_item: int = -1
        self.selected_item: int = -1

    def add_item(self, item_id: int) -> None:
        if item_id < 0 or item_id > len(Item.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        for item in self.items:
            if item.get("item") == item_id and \
                    item.get("count") < self.max_stack_count:
                item["count"] += 1
                return

        self.items.append({"item": item_id, "count": 1})

    def update(self, position: pygame.typing.SequenceLike[int | float]) -> None:
        position = pygame.Vector2(position)
        self.hovered_item = -1

        offset: pygame.Vector2 = pygame.Vector2(0, 0)
        for i in range(len(self.items)):
            if not i % self.width and i:
                offset.x = 0
                offset.y += ITEM_SIZE + 8

            item_rect = pygame.Rect(position + offset, [ITEM_SIZE, ITEM_SIZE])
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                self.hovered_item = i
                if pygame.mouse.get_pressed()[0]:
                    self.selected_item = i

            offset.x += ITEM_SIZE + 8

    def draw(self, surface: pygame.Surface, position: pygame.typing.SequenceLike[int | float]) -> None:
        position = pygame.Vector2(position)

        pygame.draw.rect(
            surface,
            (0, 0, 0, 120),
            [
                position - pygame.Vector2(8, 8),
                [(ITEM_SIZE + 8) * self.width + 8, ((len(self.items) // self.width) + 1) * (ITEM_SIZE + 8) + 8]
            ]
        )

        offset: pygame.Vector2 = pygame.Vector2(0, 0)
        for i in range(len(self.items)):
            if not i % self.width and i:
                offset.x = 0
                offset.y += ITEM_SIZE + 8

            if i == self.hovered_item:
                pygame.draw.rect(
                    surface,
                    (255, 255, 255, 90),
                    [position + offset,[ITEM_SIZE, ITEM_SIZE]]
                )

            if i == self.selected_item:
                pygame.draw.rect(
                    surface,
                    (100, 255, 100, 150),
                    [position + offset,[ITEM_SIZE, ITEM_SIZE]]
                )

            Item.draw(surface, self.items[i].get("item"), position + offset)
            surface.blit(
                FONT_18.render(str(self.items[i].get("count")), True, "#ffffff"),
                position + offset + pygame.Vector2(0, ITEM_SIZE - FONT_18.get_height())
            )

            offset.x += ITEM_SIZE + 8
