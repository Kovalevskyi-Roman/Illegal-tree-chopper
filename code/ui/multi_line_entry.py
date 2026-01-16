import pygame

from ui import MultiLineLabel
from window import Window
from common import CURSOR_BLINK_TIME


class MultiLineEntry:
    def __init__(self, rect: pygame.Rect, texture: pygame.Surface, font: pygame.Font, f_color: str) -> None:
        self.rect = rect
        self.texture = texture
        self.font = font
        self.f_color = f_color
        self.text: list[list[str]] = list(list())

        self.active: bool = False
        self.blink_timer: float = CURSOR_BLINK_TIME
        self.cursor: list[int] = [0, -1]  # [line, char]

    def set_text(self, text: str) -> None:
        self.text.clear()
        self.cursor: list[int] = [0, -1]

        for i in range(len(text.split("\n"))):
            self.text.append(list())
            self.text[i] = list(text.split("\n")[i])

    def get_line(self, index: int) -> str:
        return "".join(self.text[index])

    def get_lines(self) -> list[str]:
        return [self.get_line(i) for i in range(len(self.text))]

    def get_as_one_line(self) -> str:
        return "".join([self.get_line(i) for i in range(len(self.text))])

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
                self.cursor[1] += 1
                self.text[self.cursor[0]].insert(self.cursor[1], event.text)
                self.blink_timer += CURSOR_BLINK_TIME

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.text[self.cursor[0]] and self.cursor[1] != -1:
                        self.text[self.cursor[0]].pop(self.cursor[1])
                        self.cursor[1] -= 1

                    elif not self.text[self.cursor[0]] and self.cursor[1] == -1:
                        self.text.pop(self.cursor[0])
                        self.cursor[0] -= 1
                        if self.cursor[0] < 0:
                            self.cursor[0] = 0

                        self.cursor[1] = len(self.text[self.cursor[0]]) - 1

                    self.blink_timer += CURSOR_BLINK_TIME

                elif event.key == pygame.K_RETURN:
                    self.cursor[0] += 1
                    self.cursor[1] = -1
                    self.text.insert(self.cursor[0], list())
                    self.blink_timer += CURSOR_BLINK_TIME

                elif event.key == pygame.K_LEFT:
                    self.cursor[1] -= 1
                    if self.cursor[1] < -1:
                        self.cursor[1] = -1

                elif event.key == pygame.K_RIGHT:
                    self.cursor[1] += 1
                    if self.cursor[1] > len(self.text[self.cursor[0]]) - 1:
                        self.cursor[1] = len(self.text[self.cursor[0]]) - 1

                elif event.key == pygame.K_UP:
                    self.cursor[0] -= 1
                    if self.cursor[0] < 0:
                        self.cursor[0] = 0

                    self.cursor[1] = len(self.text[self.cursor[0]]) - 1

                elif event.key == pygame.K_DOWN:
                    self.cursor[0] += 1
                    if self.cursor[0] > len(self.text) - 1:
                        self.cursor[0] = len(self.text) - 1

                    self.cursor[1] = len(self.text[self.cursor[0]]) - 1

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect)

        MultiLineLabel(self.get_lines(), self.font, self.f_color).draw(surface, self.rect.topleft)

        width = 0
        if self.text:
            width += self.font.size(self.get_line(self.cursor[0])[:self.cursor[1] + 1])[0]

        self.blink_timer -= Window.DELTA
        if self.blink_timer < -CURSOR_BLINK_TIME:
            self.blink_timer = CURSOR_BLINK_TIME

        if self.active and self.blink_timer > 0:
            pygame.draw.rect(
                surface,
                "#ffffff",
                [self.rect.x + width,
                 self.rect.y + self.cursor[0] * self.font.get_height(), 2, self.font.get_height()]
            )

