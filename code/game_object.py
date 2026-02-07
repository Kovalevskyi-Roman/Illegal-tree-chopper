import pygame
import common

from typing import Any
from pathlib import Path
from random import choice, randint
from common import GAME_OBJECT_SIZE
from character import character_factory
from window import Window


class GameObject:
    textures: dict[str, pygame.Surface] = dict()

    @classmethod
    def init(cls) -> None:
        path: Path = Path("../resources/textures/game_objects/")

        for obj in path.iterdir():
            if not obj.is_file():
                continue

            texture = pygame.image.load(obj).convert()
            if obj.suffix == ".png":
                texture = pygame.image.load(obj).convert_alpha()

            cls.textures.setdefault(
                obj.stem,  # Имя файла
                pygame.transform.scale(texture, (GAME_OBJECT_SIZE, GAME_OBJECT_SIZE))
            )

    @classmethod
    def update(cls, game_object: dict[str, Any], *args, **kwargs) -> bool:
        """
        Обновляет один игровой объект. Возвращает True если
        текущий уровень или игровое состояние должно изменится.
        Иначе возвращает False.
        """
        player = kwargs.get("player")
        camera = kwargs.get("camera")
        level_manager = kwargs.get("level_manager")
        characters = kwargs.get("characters")
        game_state_manager = kwargs.get("game_state_manager")

        game_object_name = game_object.get("name")
        game_object_data = game_object.get("data")
        is_character: bool = game_object.get("is_character", False)
        game_object_position = pygame.Vector2(game_object_data.get("position"))
        game_object_rect = pygame.Rect(game_object_position, [GAME_OBJECT_SIZE, GAME_OBJECT_SIZE])

        if is_character:
            # Превращает game_object в character
            characters.append(character_factory(game_object))
            game_object["data"]["health"] = 0
            return False

        if game_object_name == "sapling":
            # Если саженец вырос, то он удаляет себя и добавляет дерево на своём месте
            game_object_data["grow_time"] -= Window.DELTA
            if game_object_data["grow_time"] <= 0:
                level_manager.get_current_level().game_objects.append(
                    {
                        "name": "spruce_tree",
                        "data": {
                            "position": list(game_object_position),
                            "health": 10
                        }
                    }
                )
                game_object_data["health"] = 0
            return False

        if not player.rect.colliderect(game_object_rect):
            return False

        if game_object_name == "campfire":
            player.temperature += game_object_data.get("heat")
            return False

        if not pygame.key.get_just_pressed()[pygame.K_e]:
            return False

        if "door" in game_object_name:
            level_manager.current_level = game_object_data.get("go_to")
            if game_object_data.get("player_position", None) is not None:
                player.rect.topleft = game_object_data.get("player_position")
                camera.set_offset()

            if game_object_name == "random_door":
                game_object_data["position"] = choice(game_object_data["random_positions"])
                common.game_time += randint(-300, 300)

                if randint(0, 100) < game_object_data.get("exit_chance"):
                    level_manager.current_level = game_object_data.get("exit_to")

            return True

        elif game_object_name == "bed":
            player.in_bed = not player.in_bed

        elif game_object_name == "tool_shop":
            game_state_manager.change_state(game_state_manager.TOOL_SHOP_STATE)
            return True

        elif game_object_name == "item_shop":
            game_state_manager.change_state(game_state_manager.ITEM_SHOP_STATE)
            return True

        elif game_object_name == "selling":
            while player.inventory.remove_one_item(0):
                player.money += 5

        return False

    @classmethod
    def update_objects(cls, game_objects: list[dict[str, Any]], *args, **kwargs) -> None:
        """
        Обновляет все игровые объекты на текущем уровне.
        Если cls.update() возвращает True, то все следующие объекты не обновляются.
        """
        for game_object in game_objects:
            if cls.update(game_object, *args, **kwargs):
                break

    @classmethod
    def draw(cls, surface: pygame.Surface, game_object: dict, offset: pygame.Vector2) -> None:
        """Отрисовывает один игровой объект"""
        position = pygame.Vector2(game_object.get("data").get("position"))
        screen_position = position - offset

        if screen_position.x < -GAME_OBJECT_SIZE or screen_position.x > Window.SIZE[0] or \
                screen_position.y < -GAME_OBJECT_SIZE or screen_position.y > Window.SIZE[1]:
            return

        texture = cls.textures.get(game_object.get("name"), cls.textures.get("null"))
        surface.blit(texture, screen_position)
