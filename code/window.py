import pygame

from common import FONT_18


class Window:
    SIZE: tuple[int, int] = (1280, 720)  # (1200, 675)
    FPS: int = 60
    DELTA: float = 1 / FPS

    running: bool = True
    events: tuple[pygame.event.Event, ...] = ()
    ui_surface: pygame.Surface = pygame.Surface(SIZE, flags=pygame.SRCALPHA)

    def __init__(self) -> None:
        self.surface: pygame.Surface = pygame.display.set_mode(self.SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.ui_surface.fill("#00000000")
        self.__fps_update_timer: float = 0
        self.__fps = 0

    def draw_fps(self) -> None:
        self.__fps_update_timer -= self.DELTA
        if self.__fps_update_timer <= 0:
            self.__fps = round(self.clock.get_fps())
            self.__fps_update_timer = 0.2

        self.ui_surface.blit(
            FONT_18.render(f"FPS: {self.__fps}", True, "white", "black"),
            [self.SIZE[0] - FONT_18.size(f"FPS: {self.__fps}")[0], 0]
        )

    @classmethod
    def update_events(cls) -> None:
        cls.events = tuple(pygame.event.get())

    def clear(self, color: pygame.Color | pygame.typing.SequenceLike[int] | str | int) -> None:
        self.surface.fill(color)
        self.ui_surface.fill("#00000000")

    def draw_ui(self) -> None:
        self.draw_fps()
        self.surface.blit(self.ui_surface, (0, 0))
