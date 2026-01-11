import pygame


class Window:
    SIZE: tuple[int, int] = (1280, 720)
    FPS: int = 60
    DELTA: float = 1 / FPS

    running: bool = True
    events: tuple[pygame.event.Event, ...] = ()
    ui_surface: pygame.Surface = pygame.Surface(SIZE, flags=pygame.SRCALPHA)

    def __init__(self) -> None:
        self.surface: pygame.Surface = pygame.display.set_mode(self.SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.ui_surface.fill("#00000000")

    @classmethod
    def update_events(cls) -> None:
        cls.events = tuple(pygame.event.get())

    def clear(self, color: pygame.Color | pygame.typing.SequenceLike[int] | str | int) -> None:
        self.surface.fill(color)
        self.ui_surface.fill("#00000000")

    def draw_ui(self) -> None:
        self.surface.blit(self.ui_surface, (0, 0))
