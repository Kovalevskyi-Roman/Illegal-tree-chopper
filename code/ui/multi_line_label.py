import pygame

from window import Window


class MultiLineLabel:
    def __init__(self, text: list[str], font: pygame.Font, f_color: str | int,
                 bg_color: str | pygame.typing.SequenceLike[int] | None = None, anti_aliasing: bool = True) -> None:
        self.text = text
        self.font = font
        self.f_color = f_color
        self.bg_color = bg_color
        self.anti_aliasing = anti_aliasing

        self.renders: list[pygame.Surface] = list()
        self.update()

    def update(self, text: list[str] | None = None) -> None:
        self.renders.clear()

        if text is not None:
            self.text = text

        for line in self.text:
            self.renders.append(self.font.render(line, self.anti_aliasing, self.f_color, self.bg_color))

    def draw(self, surface: pygame.Surface, position: pygame.Vector2 | pygame.typing.SequenceLike[int]) -> None:
        position = pygame.Vector2(position)

        for i in range(len(self.renders)):
            render = self.renders[i]
            # Устанавливает лейбл по центру экрана.
            label_pos = pygame.Vector2(
                Window.SIZE[0] / 2 - render.width / 2,
                Window.SIZE[1] / 2 - render.height / 2
            )
            if position.x != -1:
                label_pos.x = position.x
            if position.y != -1:
                label_pos.y = position.y

            surface.blit(render, label_pos + pygame.Vector2(0, i * self.font.get_height()))
