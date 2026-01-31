import pygame

from game_state import GameStateManager
from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window = window
        self.game_state_manager = GameStateManager()

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
            Window.update_events()
            self.update()
            self.draw()

        pygame.quit()
