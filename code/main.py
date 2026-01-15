import pygame

from object import GameObject, Tool

pygame.init()

from window import Window
from game_loop import GameLoop
from level import TileManager

def main() -> None:
    window: Window = Window()
    pygame.display.set_caption("Симулятор пьяного лесоруба")

    TileManager.init()
    GameObject.load_textures()
    Tool.init()

    GameLoop(window).run()

if __name__ == '__main__':
    main()
