import json
import pygame
import common

from random import randint
from typing import Any
from common import ITEM_SIZE


class Item:
    items: list[dict[str, Any]]= list()

    @classmethod
    def init(cls) -> None:
        with open("../resources/data/items.json", "r", encoding="utf-8") as file:
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
    def use(cls, item_index: int, *args, **kwargs) -> None:
        item = cls.items[item_index]
        player = kwargs.get("player")

        player.health += item.get("on_use").get("health", 0)
        player.temperature += item.get("on_use").get("temperature", 0)

        if item.get("name").lower() == "саженец дерева":
            kwargs.get("game_objects").append(
                {
                    "name": "sapling",
                    "data": {
                        "position": list(player.rect.topleft),
                        "grow_time": randint(15, 50)
                    }
                }
            )

    @classmethod
    def update_items(cls, *args, **kwargs) -> None:
        for item in cls.items:
            match item.get("name").lower():
                case "телефон":
                    item["description"] = [
                        f"Время: {int(common.game_time / 60)}:{round(common.game_time) % 60}",
                        f"Деньги: {common.player_money}$"
                    ]
                case "термометр":
                    temperature = kwargs.get("level").temperature
                    if kwargs.get("level").colder_at_night:
                        if common.game_time < 8 * 60:
                            temperature -= 40
                        elif common.game_time < 12 * 60 or common.game_time > 18 * 60:
                            temperature -= 20

                    item["description"] = [
                        "Температура:",
                        f"    Тела: {kwargs.get("player").temperature:.1f}",
                        f"    Локации: {temperature:.1f}"
                    ]

    @classmethod
    def draw(cls, surface: pygame.Surface, item_id: int, position: pygame.Vector2 | pygame.typing.SequenceLike[int]) -> None:
        if item_id < 0 or item_id > len(cls.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        surface.blit(cls.items[item_id].get("texture"), position)
