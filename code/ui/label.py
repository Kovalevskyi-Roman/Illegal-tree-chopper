import pygame

from window import Window


class Label:
    def __init__(self, text: str, font: pygame.Font, f_color: str | int,
                 bg_color: str | pygame.typing.SequenceLike[int] | None = None, anti_aliasing: bool = True,
                 bg_padding: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        self.text = text
        self.font = font
        self.f_color = f_color
        self.bg_color = bg_color
        self.anti_aliasing = anti_aliasing
        self.bg_padding = bg_padding

        self.render: pygame.Surface | None = None
        self.update()

    def update(self, text: str = "") -> None:
        if text:
            self.text = text
        self.render = self.font.render(self.text, self.anti_aliasing, self.f_color)

    def draw(self, surface: pygame.Surface, position: pygame.Vector2 | pygame.typing.SequenceLike[int]) -> None:
        position = pygame.Vector2(position)

        # Устанавливает лейбл по центру экрана.
        label_pos = pygame.Vector2(
            Window.SIZE[0] / 2 - self.render.width / 2,
            Window.SIZE[1] / 2 - self.render.height / 2
        )
        if position.x != -1:
            label_pos.x = position.x

        if position.y != -1:
            label_pos.y = position.y

        if self.bg_color is not None:
            pygame.draw.rect(surface, self.bg_color, [label_pos - self.bg_padding, self.render.size + self.bg_padding * 2])

        surface.blit(self.render, label_pos)
