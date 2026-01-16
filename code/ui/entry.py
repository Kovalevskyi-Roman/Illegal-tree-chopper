import pygame

from ui import Label
from window import Window
from common import CURSOR_BLINK_TIME


class Entry:
    def __init__(self, rect: pygame.Rect, texture: pygame.Surface, font: pygame.Font, f_color: str,
                 text: str = "") -> None:
        self.rect = rect
        self.texture = texture
        self.font = font
        self.f_color = f_color
        self.text: list[str] = list(text)

        self.active: bool = False
        self.blink_timer: float = CURSOR_BLINK_TIME
        self.cursor: int = -1

    def get_text(self) -> str:
        return "".join(self.text)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_just_pressed = pygame.mouse.get_just_pressed()

        if mouse_just_pressed[0] and self.rect.collidepoint(mouse_pos):
            self.active = True
            pygame.key.start_text_input()

        elif mouse_just_pressed[0]:
            self.active = False
            pygame.key.stop_text_input()

        if not self.active:
            return

        for event in Window.events:
            if event.type == pygame.TEXTINPUT:
                self.cursor += 1
                self.text.insert(self.cursor, event.text)
                self.blink_timer += CURSOR_BLINK_TIME

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.text:
                    self.text.pop(self.cursor)
                    self.cursor -= 1
                    self.blink_timer += CURSOR_BLINK_TIME

                elif event.key == pygame.K_LEFT:
                    self.cursor -= 1
                    if self.cursor < -1:
                        self.cursor = -1

                elif event.key == pygame.K_RIGHT:
                    self.cursor += 1
                    if self.cursor > len(self.text) - 1:
                        self.cursor = len(self.text) - 1

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect)
        Label("".join(self.text), self.font, self.f_color).draw(surface, self.rect.topleft)

        width = 0
        if self.text:
            width += self.font.size(self.get_text()[:self.cursor + 1])[0]

        self.blink_timer -= Window.DELTA
        if self.blink_timer < -CURSOR_BLINK_TIME:
            self.blink_timer = CURSOR_BLINK_TIME

        if self.active and self.blink_timer > 0:
            pygame.draw.rect(
                surface,
                "#ffffff",
                [self.rect.x + width,
                 self.rect.y, 2, self.font.get_ascent()]
            )
