import pygame

from typing import Any
from math import ceil
from common import ITEM_SIZE, FONT_18, FONT_20
from ui import MultiLineLabel
from window import Window
from item import Item


class Inventory:
    def __init__(self) -> None:
        self.items: list[dict[str, int]] = list()  # [{item: int, count: int}, ...]
        self.max_stack_count: int = 999
        self.max_length: int = 15
        self.width: int = 4  # количество слотов отрисовывающихся в одном ряду

        self.hovered_item: int = -1
        self.selected_item: int = -1

    def add_one_item(self, item_id: int) -> None:
        if item_id < 0 or item_id > len(Item.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        for item in self.items:
            if item.get("item") == item_id and \
                    item.get("count") < self.max_stack_count:
                item["count"] += 1
                return

        if len(self.items) < self.max_length:
            self.items.append({"item": item_id, "count": 1})

    def add_item(self, item_id: int, count: int) -> None:
        for _ in range(count):
            self.add_one_item(item_id)

    def remove_one_item(self, item_id: int) -> bool:
        """Если предмет был удалён из инвентаря возвращает True иначе False"""
        if item_id < 0 or item_id > len(Item.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        for item in self.items[::-1]:
            if item.get("item") == item_id and item.get("count") > 0:
                item["count"] -= 1
                if item.get("count") == 0:
                    self.items.remove(item)

                return True

        return False

    def remove_item(self, item_id: int, count: int) -> None:
        for _ in range(count):
            if not self.remove_one_item(item_id):
                break

    def remove_by_index(self, index: int) -> None:
        """Удаляет один предмет из инвентаря по егу индексу в инвентаре."""
        if index < 0 or index > len(self.items):
            raise IndexError(f"Inventory does not contain item with index {index}!")

        self.items[index]["count"] -= 1
        self.selected_item = -1
        self.hovered_item = -1
        if self.items[index]["count"] <= 0:
            self.items.pop(index)

    def get_selected_item(self) -> dict[str, Any] | None:
        if self.selected_item == -1:
            return None

        return self.items[self.selected_item]

    def get_hovered_item(self) -> dict[str, Any] | None:
        if self.hovered_item == -1:
            return None

        return self.items[self.hovered_item]

    def update(self, position: pygame.typing.SequenceLike[int | float]) -> None:
        position = pygame.Vector2(position)
        offset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.hovered_item = -1

        for i in range(len(self.items)):
            if not i % self.width and i:  # Если i нацело делится на self.width и не равно 0
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
        description: list = [item.get("name"), "", "", "Описание:", ""] + item.get("description")
        MultiLineLabel(description, FONT_20, "#ffffff").draw(surface, position + pygame.Vector2(4, 8))

    def draw(self, surface: pygame.Surface, position: pygame.typing.SequenceLike[int | float]) -> None:
        position = pygame.Vector2(position)
        # Фон инвентаря
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
            if not i % self.width and i:  # Если i нацело делится на self.width и не равно 0
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
