import pygame

from typing import Any
from .character import Character


class PoliceMan(Character):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self.move_speed: float = 4
        self.texture = pygame.Surface(self.rect.size)
        self.texture.fill("#232360")

        self.detect_radius: int = 300
        self.MAX_STAMINA: float = 4 * 60
        self.stamina: float = self.MAX_STAMINA
        self.is_tired: bool = False

        self.from_game_object(args[0])

    def from_game_object(self, game_object: dict[str, Any]) -> None:
        self.rect.topleft = game_object.get("data").get("position")

    def update(self, player, level_manager, *args, **kwargs) -> None:
        if self.rect.colliderect(player.rect):
            level_manager.current_level = "prison"
            return

        if self.is_tired and self.stamina < self.MAX_STAMINA:
            self.stamina += 2
        elif self.is_tired:
            self.is_tired = False

        # При преследовании игрока
        if pygame.Vector2(self.rect.topleft).distance_to(player.rect.topleft) > self.detect_radius:
            return

        self.direction = pygame.Vector2(player.rect.topleft) - self.rect.topleft
        move_speed = self.move_speed
        if self.is_tired:
            move_speed /= 2
        else:
            self.stamina -= 1

        self.rect.topleft += self.direction.normalize() * move_speed

        if self.stamina < 0:
            self.stamina = 0
            self.is_tired = True

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        surface.blit(self.texture, self.rect.topleft - offset)
