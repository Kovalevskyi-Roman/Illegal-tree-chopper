import pygame

from .multi_line_label import MultiLineLabel
from common import CURSOR_BLINK_TIME
from window import Window


class MultiLineEntry:
    def __init__(self, rect: pygame.Rect, texture: pygame.Surface, font: pygame.Font, f_color: str) -> None:
        self.rect = rect
        self.texture = texture
        self.font = font
        self.f_color = f_color
        self.text: list[list[str]] = list(list())

        self.active: bool = False
        self.blink_timer: float = CURSOR_BLINK_TIME
        self.current_line: int = 0
        self.cursor_pos: int = -1

    def set_text(self, text: str) -> None:
        self.text.clear()
        self.current_line: int = 0
        self.cursor_pos: int = -1

        for i in range(len(text.split("\n"))):
            self.text.append(list())
            self.text[i] = list(text.split("\n")[i])

    def get_line(self, index: int) -> str:
        return "".join(self.text[index])

    def get_lines(self) -> list[str]:
        return [self.get_line(i) for i in range(len(self.text))]

    def get_as_one_line(self) -> str:
        return "".join(self.get_lines())

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
            if event.type == pygame.TEXTINPUT:  # Срабатывает при печатании текста
                self.cursor_pos += 1
                self.text[self.current_line].insert(self.cursor_pos, event.text)
                self.blink_timer += CURSOR_BLINK_TIME

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Если в строке есть текст и курсор не в начале строки
                    if self.text[self.current_line] and self.cursor_pos != -1:
                        self.text[self.current_line].pop(self.cursor_pos)
                        self.cursor_pos -= 1
                    # Если в строке нет текста и курсор в начале строки
                    elif not self.text[self.current_line] and self.cursor_pos == -1:
                        self.text.pop(self.current_line)
                        self.current_line -= 1
                        if self.current_line < 0:
                            self.current_line = 0

                        self.cursor_pos = len(self.text[self.current_line]) - 1

                    self.blink_timer += CURSOR_BLINK_TIME

                # Срабатывает при нажатии Enter-а
                elif event.key == pygame.K_RETURN:
                    self.current_line += 1
                    self.cursor_pos = -1
                    self.text.insert(self.current_line, list())
                    self.blink_timer += CURSOR_BLINK_TIME

                elif event.key == pygame.K_LEFT:
                    self.cursor_pos -= 1
                    if self.cursor_pos < -1:
                        self.cursor_pos = -1

                elif event.key == pygame.K_RIGHT:
                    self.cursor_pos += 1
                    if self.cursor_pos > len(self.text[self.current_line]) - 1:
                        self.cursor_pos = len(self.text[self.current_line]) - 1

                elif event.key == pygame.K_UP:
                    self.current_line -= 1
                    if self.current_line < 0:
                        self.current_line = 0

                    self.cursor_pos = len(self.text[self.current_line]) - 1

                elif event.key == pygame.K_DOWN:
                    self.current_line += 1
                    if self.current_line > len(self.text) - 1:
                        self.current_line = len(self.text) - 1

                    self.cursor_pos = len(self.text[self.current_line]) - 1

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect)

        MultiLineLabel(self.get_lines(), self.font, self.f_color).draw(surface, self.rect.topleft)
        # Ширина текста до курсора
        width = 0
        if self.text:
            width += self.font.size(self.get_line(self.current_line)[:self.cursor_pos + 1])[0]

        self.blink_timer -= Window.DELTA
        if self.blink_timer < -CURSOR_BLINK_TIME:
            self.blink_timer = CURSOR_BLINK_TIME

        if self.active and self.blink_timer > 0:  # Отрисовывает курсор
            pygame.draw.rect(
                surface,
                "#ffffff",
                [self.rect.x + width,
                 self.rect.y + self.current_line * self.font.get_height(), 2, self.font.get_height()]
            )
