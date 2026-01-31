import json
import pygame

from typing import Any


class Tool:
    tools: list[dict[str, Any]] = list()

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
    def damage(cls, index: int) -> int | float:
        return cls.tools[index].get("damage")

    @classmethod
    def range(cls, index: int) -> int:
        return cls.tools[index].get("range")

    @classmethod
    def cool_down(cls, index: int) -> float:
        return cls.tools[index].get("cool_down")

    @classmethod
    def price(cls, index: int) -> int:
        return cls.tools[index].get("price")

    @classmethod
    def texture(cls, index: int) -> pygame.Surface:
        return cls.tools[index].get("texture")
