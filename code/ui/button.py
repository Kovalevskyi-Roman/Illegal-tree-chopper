import pygame

from collections.abc import Callable

from window import Window


class Button:
    def __init__(self, activate_func: Callable, key: int, rect: pygame.Rect, texture: pygame.Surface,
                 text: str, font: pygame.Font, f_color: str) -> None:
        self.activate_func = activate_func
        self.key = key
        self.rect = rect
        self.texture = texture
        self.text = text
        self.font = font
        self.f_color = f_color

        self.render: pygame.Surface | None = None
        self.update_render()

        if self.rect.x == -1:
            self.rect.x = Window.SIZE[0] / 2 - self.rect.width / 2

        if self.rect.y == -1:
            self.rect.y = Window.SIZE[1] / 2 - self.rect.height / 2

    def is_hovered(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_active(self) -> bool:
        return bool(self.is_hovered() and self.activate_func()[self.key])

    def update_render(self) -> None:
        self.render = self.font.render(self.text, True, self.f_color)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect.topleft)
        surface.blit(
            self.render,
            [self.rect.centerx - self.render.width / 2, self.rect.centery - self.render.height / 2]
        )
