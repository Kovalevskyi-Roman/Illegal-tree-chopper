import pygame

from typing import Any
from math import ceil
from ui import MultiLineLabel
from window import Window
from item import Item
from common import ITEM_SIZE, FONT_18, FONT_20


class Inventory:
    def __init__(self) -> None:
        # [{item: int, count: int}, ...]
        self.items: list[dict[str, int]] = list()
        self.max_stack_count: int = 999
        self.max_length: int = 15
        self.width: int = 4

        self.hovered_item: int = -1
        self.selected_item: int = -1

    def add_one_item(self, item_id: int) -> None:
        if item_id < 0 or item_id > len(Item.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        added: bool = False
        for item in self.items:
            if item.get("item") == item_id and \
                    item.get("count") < self.max_stack_count:
                item["count"] += 1
                added = True

        if len(self.items) < self.max_length and not added:
            self.items.append({"item": item_id, "count": 1})

    def add_item(self, item_id: int, count: int) -> None:
        # free slots count
        # print(self.max_lenght - ceil(count / self.max_stack_count) - len(self.items))
        for _ in range(count):
            self.add_one_item(item_id)

    def remove_one_item(self, item_id: int) -> None:
        if item_id < 0 or item_id > len(Item.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        for item in self.items:
            if item.get("item") == item_id and item.get("count") > 0:
                item["count"] -= 1
                if item.get("count") == 0:
                    self.items.remove(item)

                break

    def remove_item(self, item_id: int, count: int) -> None:
        for _ in range(count):
            self.remove_one_item(item_id)

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
                if pygame.mouse.get_just_pressed()[0]:
                    self.selected_item = i

            offset.x += ITEM_SIZE + 8

    def draw_item_data(self, surface: pygame.Surface, offset: pygame.typing.SequenceLike[int | float]) -> None:
        if self.hovered_item == -1:
            return

        offset = pygame.Vector2(offset)
        position = pygame.Vector2(Window.SIZE[0] - 300 - offset.x, offset.y)
        pygame.draw.rect(surface, (0, 0, 0, 120), [position, [300, Window.SIZE[1] - offset.y]])

        item: dict[str, Any] = Item.items[self.items[self.hovered_item].get("item")]
        text: list = [item.get("name"), "", "", "Описание:", ""] + item.get("description")
        MultiLineLabel(text, FONT_20, "#ffffff").draw(surface, position + pygame.Vector2(4, 8))

    def draw(self, surface: pygame.Surface, position: pygame.typing.SequenceLike[int | float]) -> None:
        position = pygame.Vector2(position)

        pygame.draw.rect(
            surface,
            (0, 0, 0, 120),
            [
                position - pygame.Vector2(8, 8),
                [(ITEM_SIZE + 8) * self.width + 8, ceil(len(self.items) / self.width) * (ITEM_SIZE + 8) + 8]
            ]
        )

        offset: pygame.Vector2 = pygame.Vector2(0, 0)
        for i in range(len(self.items)):
            if not i % self.width and i:
                offset.x = 0
                offset.y += ITEM_SIZE + 8

            if i == self.hovered_item:
                pygame.draw.rect(
                    surface, (255, 255, 255, 90), [position + offset,[ITEM_SIZE, ITEM_SIZE]]
                )

            if i == self.selected_item:
                pygame.draw.rect(
                    surface, (100, 255, 100, 150), [position + offset,[ITEM_SIZE, ITEM_SIZE]]
                )

            Item.draw(surface, self.items[i].get("item"), position + offset)
            if self.items[i].get("count") > 1:
                surface.blit(
                    FONT_18.render(str(self.items[i].get("count")), True, "#ffffff"),
                    position + offset + pygame.Vector2(0, ITEM_SIZE - FONT_18.get_height())
                )

            offset.x += ITEM_SIZE + 8
