import pygame

from game_state import GameStateManager
from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window = window
        self.game_state_manager = GameStateManager()

    def event_loop(self) -> None:
        Window.update_events()
        for event in Window.events:
            if event.type == pygame.QUIT:
                Window.running = False

    def update(self) -> None:
        self.window.clock.tick(Window.FPS)  # Устанавливает FPS игры на значение Window.FPS
        self.game_state_manager.update()

    def draw(self) -> None:
        self.window.clear("#000000")

        self.game_state_manager.draw(self.window.surface)
        self.window.draw_ui()

        pygame.display.update()

    def run(self) -> None:
        while Window.running:
            self.update()
            self.draw()
            self.event_loop()

        pygame.quit()
