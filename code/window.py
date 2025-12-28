import pygame


class Window:
    SIZE: tuple[int, int] = (1120, 630)
    FPS: int = 60
    events: tuple[pygame.event.Event, ...] = ()

    def __init__(self) -> None:
        self.surface: pygame.Surface = pygame.display.set_mode(self.SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()

    @classmethod
    def update_events(cls) -> None:
        cls.events = tuple(pygame.event.get())

    def clear(self, color: pygame.Color | pygame.typing.SequenceLike[int] | str | int) -> None:
        self.surface.fill(color)
