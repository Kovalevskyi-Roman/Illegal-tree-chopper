import json
import pygame

from typing import Any
from common import ITEM_SIZE


class Item:
    items: list[dict[str, Any]]= list()

    @classmethod
    def init(cls) -> None:
        with open("../resources/data/items.json", "r") as file:
            cls.items = json.load(file)

        for item in cls.items:
            if not item["texture"]:
                continue
            item["texture"] = pygame.image.load("../resources/textures/items/" + item["texture"]).convert_alpha()
            item["texture"] = pygame.transform.scale(item["texture"], [ITEM_SIZE, ITEM_SIZE])

    @classmethod
    def can_use(cls, item_index: int) -> bool:
        return cls.items[item_index].get("on_use", None) is not None

    @classmethod
    def use(cls, item_index: int) -> None:
        ...

    @classmethod
    def draw(cls, surface: pygame.Surface, item_id: int, position: pygame.Vector2 | pygame.typing.SequenceLike[int]) -> None:
        if item_id < 0 or item_id > len(cls.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        surface.blit(cls.items[item_id].get("texture"), position)
