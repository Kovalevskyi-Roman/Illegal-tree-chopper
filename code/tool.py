import json
import pygame

from typing import Any
from random import randint
from common import GAME_OBJECT_SIZE
from window import Window


class Tool:
    tools: list[dict[str, Any]] = list()
    cool_down: float = 0

    @classmethod
    def init(cls) -> None:
        try:
            with open("../resources/data/tools.json", "r", encoding="utf-8") as file:
                cls.tools = json.load(file)

            for tool in cls.tools:
                tool["texture"] = pygame.image.load(f"../resources/textures/tools/{tool.get("texture")}").convert_alpha()
                tool["texture"] = pygame.transform.scale2x(tool["texture"])
                tool["texture"] = pygame.transform.rotate(tool["texture"], 90)

        except FileNotFoundError:
            print("ERROR: File 'tools.json' not found.")

    @classmethod
    def get_damage(cls, index: int) -> int | float:
        return cls.tools[index].get("damage")

    @classmethod
    def get_range(cls, index: int) -> int:
        return cls.tools[index].get("range")

    @classmethod
    def get_cool_down(cls, index: int) -> float:
        return cls.tools[index].get("cool_down")

    @classmethod
    def get_price(cls, index: int) -> int:
        return cls.tools[index].get("price")

    @classmethod
    def get_texture(cls, index: int) -> pygame.Surface:
        return cls.tools[index].get("texture")

    @classmethod
    def update_cool_down(cls) -> None:
        if cls.cool_down > 0:
            cls.cool_down -= Window.DELTA
        else:
            cls.cool_down = 0

    @classmethod
    def attack_tree(cls, game_objects: list[dict[str, Any]], offset: pygame.Vector2, player) -> None:
        cls.cool_down = cls.get_cool_down(player.tool)
        for game_object in game_objects:
            # Если game_object не дерево, то скип
            if "tree" not in game_object.get("name"):
                continue

            game_object_position = pygame.Vector2(game_object.get("data").get("position"))
            game_object_rect = pygame.Rect(game_object_position - offset, [GAME_OBJECT_SIZE, GAME_OBJECT_SIZE])
            game_object_center = game_object_position + pygame.Vector2(GAME_OBJECT_SIZE / 2, GAME_OBJECT_SIZE / 2)

            # Если дерево слишком далеко от игрока
            if game_object_center.distance_to(player.rect.center) > Tool.get_range(player.tool):
                continue

            # Если курсор наведён на дерево
            if game_object_rect.collidepoint(pygame.mouse.get_pos()):
                game_object["data"]["health"] -= Tool.get_damage(player.tool)

                # Если дерево было срублено
                if game_object.get("data").get("health") <= 0:
                    player.trees_chopped += 1
                    player.inventory.add_item(0, randint(1, 5) * int(Tool.get_damage(player.tool)))
