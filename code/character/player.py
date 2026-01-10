import pygame

from .character import Character


class Player(Character):
    def __init__(self) -> None:
        super().__init__()

        self.move_speed: float = 4

    def update(self) -> None:
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
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

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "#aaaaaa", [self.rect.topleft - offset, self.rect.size])
