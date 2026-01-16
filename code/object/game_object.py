import pygame

from pathlib import Path
from typing import Any

from window import Window


class GameObject:
    SIZE: int = 48
    textures: dict[str, pygame.Surface] = dict()

    @classmethod
    def load_textures(cls) -> None:
        path: Path = Path("../resources/textures/game_objects/")

        for obj in path.iterdir():
            if not obj.is_file():
                continue

            if obj.suffix == ".png":
                texture = pygame.image.load(obj).convert_alpha()
                cls.textures.setdefault(obj.stem, pygame.transform.scale(texture, (cls.SIZE, cls.SIZE)))
            else:
                texture = pygame.image.load(obj).convert()
                cls.textures.setdefault(obj.stem, pygame.transform.scale(texture, (cls.SIZE, cls.SIZE)))

    @classmethod
    def update(cls, game_object: dict[str, Any], *args, **kwargs) -> bool:
        player = kwargs.get("player")
        camera = kwargs.get("camera")
        level_manager = kwargs.get("level_manager")

        game_object_name = game_object.get("name")
        game_object_position = pygame.Vector2(game_object.get("data").get("position"))
        game_object_rect = pygame.Rect(game_object_position, [cls.SIZE, cls.SIZE])

        if game_object_name == "door":
            if player.rect.colliderect(game_object_rect) and \
                    pygame.key.get_just_pressed()[pygame.K_e]:

                if game_object.get("data").get("player_position", None) is not None:
                    player.rect.topleft = game_object.get("data").get("player_position")
                    camera.set_offset()

                level_manager.current_level = game_object.get("data").get("go_to")
                return True

        elif game_object_name == "campfire":
            if pygame.Vector2(game_object_rect.center).distance_to(player.rect.center) <= cls.SIZE:
                player.temperature += game_object.get("data").get("heat")

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

        if screen_position.x < -cls.SIZE or screen_position.x > Window.SIZE[0] or \
                screen_position.y < -cls.SIZE or screen_position.y > Window.SIZE[1]:
            return

        texture = cls.textures.get(game_object.get("name"), None)
        if texture is not None:
            surface.blit(texture, screen_position)
