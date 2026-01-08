import pygame

from player import Player
from window import Window
from level import TileMap


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window = window

        self.player = Player()
        self.tile_map = TileMap("test")

        self.running: bool = True

    def event_loop(self) -> None:
        Window.update_events()
        for event in Window.events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.window.clock.tick(Window.FPS)
        self.player.update()

    def draw(self) -> None:
        self.window.clear("#000000")
        self.tile_map.draw(self.window.surface)
        self.player.draw(self.window.surface)
        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.update()
            self.draw()
            self.event_loop()

        pygame.quit()
