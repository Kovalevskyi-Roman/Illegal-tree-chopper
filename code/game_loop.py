import pygame

from camera import Camera
from character import Player
from window import Window
from level import LevelManager


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window = window

        self.player = Player()
        self.camera = Camera(self.player)
        self.level_manager = LevelManager(self.player, self.camera)

        self.running: bool = True

    def event_loop(self) -> None:
        Window.update_events()
        for event in Window.events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.window.clock.tick(Window.FPS)
        self.level_manager.update_level()

    def draw(self) -> None:
        self.window.clear("#000000")
        self.level_manager.draw_level(self.window.surface)
        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.update()
            self.draw()
            self.event_loop()

        pygame.quit()
