import pygame

from typing import Any
from tool import Tool
from common import GAME_OBJECT_SIZE, TILE_SIZE
from ui import MultiLineLabel
from window import Window
from inventory import Inventory
from .character import Character


class Player(Character):
    def __init__(self) -> None:
        super().__init__()

        self.rect.x = TILE_SIZE * 8
        self.rect.y = TILE_SIZE * 8

        self.move_speed: float = 4
        self.cool_down: float = 0
        self.last_direction: pygame.Vector2 = pygame.Vector2(0, 0)

        self.cold_protection: float = 1
        self.temperature: float = 36
        self.temperature_update_timer: float = 0

        self.time: float = 0  # seconds
        self.tool: int = 0
        self.inventory_opened: bool = False
        self.inventory: Inventory = Inventory()
        self.inventory.max_stack_count = 5

        self.stats_lbl: MultiLineLabel = MultiLineLabel(
            [
                f"Время: {int(self.time / 60)}:{round(self.time) % 60}",
                f"Здоровье: {self.health}",
                f"Температура: {self.temperature:.1f}"
            ],
            pygame.font.SysFont("Tahoma", 22),
            "#ffffff",
            "#323232"
        )

    def attack_tree(self, game_objects: list[dict[str, Any]], offset: pygame.Vector2) -> None:
        self.cool_down = Tool.cool_down(self.tool)
        for game_object in game_objects:
            if "tree" not in game_object.get("name"):
                continue

            game_object_position = pygame.Vector2(game_object.get("data").get("position"))
            game_object_rect = pygame.Rect(game_object_position - offset, [GAME_OBJECT_SIZE, GAME_OBJECT_SIZE])
            game_object_center = game_object_position + pygame.Vector2(GAME_OBJECT_SIZE / 2, GAME_OBJECT_SIZE / 2)

            if game_object_center.distance_to(self.rect.center) > Tool.range(self.tool):
                continue

            if game_object_rect.collidepoint(pygame.mouse.get_pos()):
                game_object["data"]["health"] -= Tool.damage(self.tool)

    def update_temperature(self, level_temperature: int) -> None:
        if level_temperature < 4:
            level_temperature /= self.cold_protection

        self.temperature += (level_temperature - self.temperature) / 1000
        self.temperature = round(self.temperature, 3)

        if self.temperature < 4:
            self.health -= 0.1
            self.health = round(self.health, 1)
        elif self.temperature >= 39:
            self.health -= 0.2
            self.health = round(self.health, 1)

    def update(self, game_objects: list[dict[str, Any]], offset: pygame.Vector2, level_temperature: int) -> None:
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        # movement
        if self.direction.x:
            self.last_direction.x = self.direction.x
        if self.direction.y:
            self.last_direction.y = self.direction.y

        self.direction = pygame.Vector2(0, 0)
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1

        if pygame.key.get_just_pressed()[pygame.K_TAB]:
            self.inventory_opened = not self.inventory_opened

        if self.inventory_opened:
            self.inventory.update([32, 32])
        else:
            self.inventory.selected_item = -1

        if self.direction.length() and not self.inventory_opened:
            self.rect.topleft += self.direction.normalize() * self.move_speed

        self.temperature_update_timer -= Window.DELTA
        if self.temperature_update_timer <= 0:
            self.update_temperature(level_temperature)
            self.temperature_update_timer = 0.1

        self.time += Window.DELTA
        if self.time >= 24 * 60:
            self.time = 0

        if self.cool_down > 0:
            self.cool_down -= Window.DELTA
        else:
            self.cool_down = 0

        if not self.cool_down and pygame.mouse.get_pressed()[0] and not self.inventory_opened:
            self.attack_tree(game_objects, offset)

    def draw_tool(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        texture = Tool.texture(self.tool)
        position = self.rect.topleft - pygame.Vector2(self.rect.width, 0) - offset

        if self.cool_down:
            texture = pygame.transform.rotate(texture, 90)

        if self.last_direction.x > 0:
            position = self.rect.topright - offset
            texture = pygame.transform.flip(texture, True, False)

        surface.blit(texture, position)

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "#aaaaaa", [self.rect.topleft - offset, self.rect.size])

        self.draw_tool(surface, offset)

        if self.inventory_opened:
            self.inventory.draw(Window.ui_surface, [32, 32])

        # self.stats_lbl.update(
        #     [
        #         f"Время: {int(self.time / 60)}:{round(self.time) % 60}",
        #         f"Здоровье: {self.health}",
        #         f"Температура: {self.temperature:.1f}"
        #     ]
        # )
        # self.stats_lbl.draw(Window.ui_surface, [0, 0])
