import pygame


class Character:
    """Базовый класс персонажа."""
    def __init__(self) -> None:
        self.health: float = 100

        self.rect: pygame.FRect = pygame.FRect(0, 0, 32, 32)
        self.direction: pygame.Vector2 = pygame.Vector2(0, 0)

    def update(self, *args, **kwargs) -> None:
        ...

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        ...
