import pygame
import common

from pathlib import Path
from typing import Any
from common import GAME_OBJECT_SIZE
from character import Chest
from window import Window


class GameObject:
    textures: dict[str, pygame.Surface] = dict()

    @classmethod
    def load_textures(cls) -> None:
        path: Path = Path("../resources/textures/game_objects/")

        for obj in path.iterdir():
            if not obj.is_file():
                continue

            if obj.suffix == ".png":
                texture = pygame.image.load(obj).convert_alpha()
                cls.textures.setdefault(obj.stem, pygame.transform.scale(texture, (GAME_OBJECT_SIZE, GAME_OBJECT_SIZE)))
            else:
                texture = pygame.image.load(obj).convert()
                cls.textures.setdefault(obj.stem, pygame.transform.scale(texture, (GAME_OBJECT_SIZE, GAME_OBJECT_SIZE)))

    @classmethod
    def update(cls, game_object: dict[str, Any], *args, **kwargs) -> bool:
        player = kwargs.get("player")
        camera = kwargs.get("camera")
        level_manager = kwargs.get("level_manager")
        characters = kwargs.get("characters")
        game_state_manager = kwargs.get("game_state_manager")

        game_object_name = game_object.get("name")
        game_object_position = pygame.Vector2(game_object.get("data").get("position"))
        game_object_rect = pygame.Rect(game_object_position, [GAME_OBJECT_SIZE, GAME_OBJECT_SIZE])

        if game_object_name == "door":
            if player.rect.colliderect(game_object_rect) and \
                    pygame.key.get_just_pressed()[pygame.K_e]:

                if game_object.get("data").get("player_position", None) is not None:
                    player.rect.topleft = game_object.get("data").get("player_position")
                    camera.set_offset()

                level_manager.current_level = game_object.get("data").get("go_to")
                return True

        elif game_object_name == "campfire":
            if pygame.Vector2(game_object_rect.center).distance_to(player.rect.center) <= GAME_OBJECT_SIZE:
                player.temperature += game_object.get("data").get("heat")

        elif game_object_name == "bed":
            if player.rect.colliderect(game_object_rect):
                if pygame.key.get_just_pressed()[pygame.K_e]:
                    player.in_bed = not player.in_bed

                if player.in_bed:
                    player.direction = pygame.Vector2(0, 0)
                    common.game_time += 0.25

        elif game_object_name == "chest":
            chest = Chest()
            chest.from_game_object(game_object)
            characters.append(chest)
            game_object["data"]["health"] = 0

        elif game_object_name == "tool_shop":
            if player.rect.colliderect(game_object_rect) and \
                    pygame.key.get_just_pressed()[pygame.K_e]:
                game_state_manager.change_state(game_state_manager.TOOL_SHOP_STATE)
                return True

        elif game_object_name == "item_shop":
            if player.rect.colliderect(game_object_rect) and \
                    pygame.key.get_just_pressed()[pygame.K_e]:
                game_state_manager.change_state(game_state_manager.ITEM_SHOP_STATE)
                return True

        elif game_object_name == "selling":
            if player.rect.colliderect(game_object_rect) and \
                    pygame.key.get_just_pressed()[pygame.K_e]:

                while player.inventory.remove_one_item(0):
                    common.player_money += 5

        elif game_object_name == "sapling":
            game_object.get("data")["grow_time"] -= Window.DELTA
            if game_object.get("data")["grow_time"] <= 0:
                level_manager.get_current_level().game_objects.append(
                    {
                        "name": "spruce_tree",
                        "data": {
                            "position": list(game_object_position),
                            "health": 10
                        }
                    }
                )
                game_object.get("data")["health"] = 0

        return False

    @classmethod
    def update_objects(cls, game_objects: list[dict[str, Any]], *args, **kwargs) -> None:
        for game_object in game_objects:
            if cls.update(game_object, *args, **kwargs):
                break

    @classmethod
    def draw(cls, surface: pygame.Surface, game_object: dict, offset: pygame.Vector2) -> None:
        position = pygame.Vector2(game_object.get("data").get("position"))
        screen_position = position - offset

        if screen_position.x < -GAME_OBJECT_SIZE or screen_position.x > Window.SIZE[0] or \
                screen_position.y < -GAME_OBJECT_SIZE or screen_position.y > Window.SIZE[1]:
            return

        texture = cls.textures.get(game_object.get("name"), None)
        if texture is not None:
            surface.blit(texture, screen_position)
