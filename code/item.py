import json
import pygame
import common

from typing import Any
from random import randint
from common import ITEM_SIZE


class Item:
    items: list[dict[str, Any]] = list()

    @classmethod
    def init(cls) -> None:
        try:
            with open("../resources/data/items.json", "r", encoding="utf-8") as file:
                cls.items = json.load(file)

            for item in cls.items:
                if not item["texture"]:
                    continue
                item["texture"] = pygame.image.load(f"../resources/textures/items/{item["texture"]}").convert_alpha()
                item["texture"] = pygame.transform.scale(item["texture"], [ITEM_SIZE, ITEM_SIZE])

        except FileNotFoundError:
            print("ERROR: File 'items.json' not found.")

    @classmethod
    def can_use(cls, item_index: int) -> bool:
        return cls.items[item_index].get("on_use", None) is not None

    @classmethod
    def is_spend(cls, item_index: int) -> bool:
        return cls.items[item_index].get("is_spend", True)

    @classmethod
    def use(cls, item_index: int, *args, **kwargs) -> None:
        item = cls.items[item_index]
        player = kwargs.get("player")
        game_objects: list[dict] = kwargs.get("game_objects")
        level_manager = kwargs.get("level_manager")

        player.health += item.get("on_use").get("health", 0)
        player.temperature += item.get("on_use").get("temperature", 0)

        match item.get("name").lower():
            case "саженец дерева":
                player.trees_planted += 1
                game_objects.append(
                    {
                        "name": "sapling",
                        "data": {
                            "position": list(player.rect.topleft),
                            "grow_time": randint(15, 50)
                        }
                    }
                )

            case "улучшение инвентаря":
                player.inventory.max_stack_count += 1
                player.inventory.restack()

            case "улучшение термозащиты":
                player.cold_protection += 1

            case "фотоаппарат":
                player.inventory.selected_item = -1
                player.rect.topleft = [144, 288]
                level_manager.camera.set_offset()
                level_manager.current_level = "backrooms"

    @classmethod
    def update_items(cls, *args, **kwargs) -> None:
        for item in cls.items:
            match item.get("name").lower():
                case "телефон":
                    item["description"] = [
                        f"Время: {int(common.game_time / 60)}:{int(common.game_time) % 60}",
                        f"Деньги: {kwargs.get("player").money}$"
                    ]
                case "термометр":
                    item["description"] = [
                        "Температура:",
                        f"    Тела: {kwargs.get("player").temperature:.1f}",
                        f"    Локации: {kwargs.get("level").temperature:.1f}"
                    ]

    @classmethod
    def draw(cls, surface: pygame.Surface, item_id: int, position: pygame.Vector2 | pygame.typing.SequenceLike[int]) -> None:
        if item_id < 0 or item_id > len(cls.items):
            raise ValueError(f"Item with id {item_id} does not exist!")

        surface.blit(cls.items[item_id].get("texture"), position)
