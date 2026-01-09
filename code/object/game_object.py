import pygame

from pathlib import Path


class GameObject:
    SIZE: int = 32
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
    def update(cls, game_object: dict, *args, **kwargs) -> None:
        match game_object.get("name"):
            case "apple":
                if kwargs.get("player").rect.colliderect([game_object.get("data").get("position"), [cls.SIZE, cls.SIZE]]):
                    kwargs.get("level_manager").current_level = "aboba"

    @classmethod
    def draw(cls, surface: pygame.Surface, game_object: dict, offset: pygame.Vector2) -> None:
        texture = cls.textures.get(game_object.get("name"), None)
        if texture is not None:
            surface.blit(texture, pygame.Vector2(game_object.get("data").get("position")) - offset)
