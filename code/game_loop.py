import pygame

from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window = window

        self.running: bool = True

    def event_loop(self) -> None:
        Window.update_events()
        for event in Window.events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.window.clock.tick(Window.FPS)

    def draw(self) -> None:
        pygame.display.update()
        self.window.clear("#000000")

    def run(self) -> None:
        while self.running:
            self.update()
            self.draw()
            self.event_loop()

        pygame.quit()
