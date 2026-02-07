import pygame
import common

from typing import Any
from .character import Character
from item import Item
from tool import Tool
from ui import MultiLineLabel
from window import Window
from inventory import Inventory


class Player(Character):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self.rect.x = 480
        self.rect.y = 336
        self.move_speed: float = 4
        self.last_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.in_bed: bool = False
        self.in_chest: bool = False
        self.money: int = 2000

        self.cold_protection: float = 1
        self.temperature: float = 36
        self.temperature_update_timer: float = 0

        self.tool: int = 0  # Id текущего инструмента
        self.trees_chopped: int = 0
        self.trees_planted: int = 0

        self.inventory_opened: bool = False
        self.inventory: Inventory = Inventory()
        self.inventory.max_length = 15
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

    def __update_temperature(self, level_temperature: int) -> None:
        # Применение защиты от холода
        if level_temperature < 4:
            level_temperature /= self.cold_protection

        # Обновление температуры
        self.temperature += (level_temperature - self.temperature) / 1000
        self.temperature = round(self.temperature, 3)

        # Опасная температура при которой игрок получает урон
        if self.temperature < 4 or self.temperature >= 39:
            self.health -= 0.75
            self.health = round(self.health, 1)

        # Чем меньше температура игрока тем больше непрозрачность текстуры замерзания
        if self.temperature > 3:
            self.__froze_texture.set_alpha(int((255 / (self.temperature * 10)) * (1 / self.temperature) * 150))
        else:
            self.__froze_texture.set_alpha(255)

    def update(self, game_objects: list[dict[str, Any]], offset: pygame.Vector2,
               level_temperature: int, colder_at_night: bool, level_manager: "LevelManager") -> None:
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
            selected_item = self.inventory.get_selected_item()
            if selected_item is not None and Item.can_use(selected_item.get("item")) and not self.in_chest:
                Item.use(
                    selected_item.get("item"),
                    player=self,
                    game_objects=game_objects,
                    level_manager=level_manager
                )
                # Потратится ли предмет при использовании
                if Item.is_spend(selected_item.get("item")):
                    self.inventory.remove_by_index(self.inventory.selected_item)

        # Обновление позиции игрока
        if self.direction.length() and not self.inventory_opened and not self.in_bed:
            self.rect.topleft += self.direction.normalize() * self.move_speed

        # Обновляет температуру игрока каждые 100 миллисекунд
        self.temperature_update_timer -= Window.DELTA
        if self.temperature_update_timer <= 0:
            self.__update_temperature(level_temperature)
            self.temperature_update_timer = 0.1

        if self.in_bed:
            common.game_time += 0.25

        Tool.update_cool_down()

        # Атакует ли игрок дерево
        if not Tool.cool_down and pygame.mouse.get_pressed()[0] and not self.inventory_opened:
            Tool.attack_tree(game_objects, offset, self)

    def __draw_tool(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        texture = Tool.get_texture(self.tool)
        position = self.rect.topleft - pygame.Vector2(self.rect.width, 0) - offset

        # Если идёт перезарядка
        if Tool.cool_down > Window.DELTA:
            texture = pygame.transform.rotate(texture, 90)

        # Если игрок смотрит вправо отрисовывает инструмент справа от игрока
        # (По умолчанию инструмент отрисовывается слева от игрока)
        if self.last_direction.x > 0:
            position = self.rect.topright - offset
            texture = pygame.transform.flip(texture, True, False)

        surface.blit(texture, position)

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "#aaaaaa", [self.rect.topleft - offset, self.rect.size])

        self.__draw_tool(surface, offset)

        if self.inventory_opened:
            self.inventory.draw(Window.ui_surface, [32, 32])
            self.inventory.draw_item_data(Window.ui_surface, [16, 16])

        Window.ui_surface.blit(self.__froze_texture, [0, 0])

        self.stats_lbl.update([f"Здоровье: {self.health}"])
        self.stats_lbl.draw(Window.ui_surface, [0, 0])
