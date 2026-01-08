import pygame

from camera import Camera
from character.player import Player
from window import Window
from level import TileMap


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window = window

        self.player = Player()
        self.camera = Camera(self.player)
        self.tile_map = TileMap("test")

        self.running: bool = True

    def event_loop(self) -> None:
        Window.update_events()
        for event in Window.events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.window.clock.tick(Window.FPS)
        self.camera.update()
        self.player.update()

    def draw(self) -> None:
        self.window.clear("#000000")
        self.tile_map.draw(self.window.surface, self.camera.offset)
        self.player.draw(self.window.surface, self.camera.offset)
        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.update()
            self.draw()
            self.event_loop()

        pygame.quit()
