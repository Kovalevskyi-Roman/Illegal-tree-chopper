from typing import Any

import pygame

from object import GameObject
from window import Window
from .character import Character


class Player(Character):
    def __init__(self) -> None:
        super().__init__()

        self.move_speed: float = 4

        self.tool_damage: float = 1
        self.tool_range: float = 40
        self.tool_cool_down: float = 2
        self.cool_down: float = 0

    def attack_tree(self, game_objects: list[dict[str, Any]], offset: pygame.Vector2) -> None:
        self.cool_down = self.tool_cool_down
        for game_object in game_objects:
            if "tree" not in game_object.get("name"):
                continue
            game_object_position = pygame.Vector2(game_object.get("data").get("position"))
            game_object_rect = pygame.Rect(game_object_position - offset, [GameObject.SIZE, GameObject.SIZE])

            if (game_object_position + pygame.Vector2(GameObject.SIZE / 2, GameObject.SIZE / 2)).distance_to(self.rect.center) > self.tool_range:
                continue

            if game_object_rect.collidepoint(pygame.mouse.get_pos()):
                game_object["data"]["health"] -= self.tool_damage
                print(f"Hit! {game_object.get("data").get("health")}hp left!")

    def update(self, game_objects: list[dict[str, Any]], offset: pygame.Vector2) -> None:
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        # movement
        self.direction = pygame.Vector2(0, 0)
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1

        if self.direction.length():
            self.rect.topleft += self.direction.normalize() * self.move_speed

        if self.cool_down > 0:
            self.cool_down -= Window.DELTA
        else:
            self.cool_down = 0

        if not self.cool_down and pygame.mouse.get_pressed()[0]:
            self.attack_tree(game_objects, offset)

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "#aaaaaa", [self.rect.topleft - offset, self.rect.size])
