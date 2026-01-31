import pygame
import common

from random import randint
from typing import Any
from .character import Character
from common import GAME_OBJECT_SIZE
from item import Item
from tool import Tool
from ui import MultiLineLabel
from window import Window
from inventory import Inventory


class Player(Character):
    def __init__(self) -> None:
        super().__init__()

        self.rect.x = 480
        self.rect.y = 336
        self.move_speed: float = 4
        self.last_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.in_bed: bool = False

        self.cold_protection: float = 1
        self.temperature: float = 36
        self.temperature_update_timer: float = 0

        self.tool: int = 0  # Id текущего инструмента
        self.tool_cool_down: float = 0
        self.trees_chopped: int = 0
        self.trees_planted: int = 0

        self.inventory_opened: bool = False
        self.inventory: Inventory = Inventory()
        self.inventory.max_stack_count = 5
        # Добавляет телефон и термометр в инвентарь
        self.inventory.add_one_item(1)
        self.inventory.add_one_item(2)

        self.stats_lbl: MultiLineLabel = MultiLineLabel(
            [f"Здоровье: {self.health}"],
            pygame.font.SysFont("Tahoma", 22),
            "#ffffff",
            "#323232"
        )
        # Текстура замерзания игрока
        self.__froze_texture = pygame.image.load("../resources/textures/frozen_effect.png").convert_alpha()
        self.__froze_texture = pygame.transform.scale(self.__froze_texture, Window.SIZE)
        self.__froze_texture.set_alpha(0)

    def attack_tree(self, game_objects: list[dict[str, Any]], offset: pygame.Vector2) -> None:
        self.tool_cool_down = Tool.cool_down(self.tool)
        for game_object in game_objects:
            # Если game_object не дерево, то скип
            if "tree" not in game_object.get("name"):
                continue

            game_object_position = pygame.Vector2(game_object.get("data").get("position"))
            game_object_rect = pygame.Rect(game_object_position - offset, [GAME_OBJECT_SIZE, GAME_OBJECT_SIZE])
            game_object_center = game_object_position + pygame.Vector2(GAME_OBJECT_SIZE / 2, GAME_OBJECT_SIZE / 2)

            # Если дерево слишком далеко от игрока
            if game_object_center.distance_to(self.rect.center) > Tool.range(self.tool):
                continue

            # Если курсор наведён на дерево
            if game_object_rect.collidepoint(pygame.mouse.get_pos()):
                game_object["data"]["health"] -= Tool.damage(self.tool)

                # Если дерево было срублено
                if game_object.get("data").get("health") <= 0:
                    self.trees_chopped += 1
                    self.inventory.add_item(0, randint(1, 5) * int(Tool.damage(self.tool)))

    def update_temperature(self, level_temperature: int, colder_at_night: bool) -> None:
        # Меняется ли температура на уровне при изменении игрового времени
        if colder_at_night:
            if common.game_time < 6 * 60:  # До 6 утра
                level_temperature -= 40
            elif common.game_time < 10 * 60 or common.game_time > 19 * 60:  # До 10 утра или после 7 вечера
                level_temperature -= 30

        # Применение защиты от холода
        if level_temperature < 4:
            level_temperature /= self.cold_protection

        # Обновление температуры
        self.temperature += (level_temperature - self.temperature) / 1000
        self.temperature = round(self.temperature, 3)

        # Опасная температура при которой игрок получает урон
        if self.temperature < 6 or self.temperature >= 39:
            self.health -= 0.75
            self.health = round(self.health, 1)

        # Чем меньше температура игрока тем больше непрозрачность текстуры замерзания
        if self.temperature > 0:
            self.__froze_texture.set_alpha(int((255 / (self.temperature * 10)) * (1 / self.temperature) * 150))
        else:
            self.__froze_texture.set_alpha(255)

    def update(self, game_objects: list[dict[str, Any]], offset: pygame.Vector2,
               level_temperature: int, colder_at_night: bool) -> None:
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        # Последнее направление движения игрока
        if self.direction.x:
            self.last_direction.x = self.direction.x
        if self.direction.y:
            self.last_direction.y = self.direction.y

        # Передвижение игрока
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

        # Обновление инвентаря
        if self.inventory_opened:
            self.inventory.update([32, 32])
            # Может ли игрок использовать предмет
            if self.inventory.selected_item != -1:
                if Item.can_use(self.inventory.get_selected_item().get("item")):
                    Item.use(
                        self.inventory.get_selected_item().get("item"),
                        player=self,
                        game_objects=game_objects
                    )
                    self.inventory.remove_by_index(self.inventory.selected_item)

        # Обновление позиции игрока
        if self.direction.length() and not self.inventory_opened and not self.in_bed:
            self.rect.topleft += self.direction.normalize() * self.move_speed

        # Обновляет температуру игрока каждые 100 миллисекунд
        self.temperature_update_timer -= Window.DELTA
        if self.temperature_update_timer <= 0:
            self.update_temperature(level_temperature, colder_at_night)
            self.temperature_update_timer = 0.1

        # Обновляет перезарядку инструмента
        if self.tool_cool_down > 0:
            self.tool_cool_down -= Window.DELTA
        else:
            self.tool_cool_down = 0

        # Атакует ли игрок дерево
        if not self.tool_cool_down and pygame.mouse.get_pressed()[0] and not self.inventory_opened:
            self.attack_tree(game_objects, offset)

    def draw_tool(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        texture = Tool.texture(self.tool)
        position = self.rect.topleft - pygame.Vector2(self.rect.width, 0) - offset

        # Если идёт перезарядка
        if self.tool_cool_down > Window.DELTA:
            texture = pygame.transform.rotate(texture, 90)

        # Если игрок смотрит вправо отрисовывает инструмент справа от игрока
        # (По умолчанию инструмент отрисовывается слева от игрока)
        if self.last_direction.x > 0:
            position = self.rect.topright - offset
            texture = pygame.transform.flip(texture, True, False)

        surface.blit(texture, position)

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "#aaaaaa", [self.rect.topleft - offset, self.rect.size])

        self.draw_tool(surface, offset)

        if self.inventory_opened:
            self.inventory.draw(Window.ui_surface, [32, 32])
            self.inventory.draw_item_data(Window.ui_surface, [16, 16])

        Window.ui_surface.blit(self.__froze_texture, [0, 0])

        self.stats_lbl.update([f"Здоровье: {self.health}"])
        self.stats_lbl.draw(Window.ui_surface, [0, 0])
