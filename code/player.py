import pygame


class Player:
    def __init__(self) -> None:
        self.health: int = 100

        self.rect: pygame.FRect = pygame.FRect(0, 0, 32, 32)
        self.move_speed: float = 4
        self.direction: pygame.Vector2 = pygame.Vector2(0, 0)

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

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "white", self.rect)
