import pygame

from object import GameObject

pygame.init()

from window import Window
from game_loop import GameLoop
from level import TileManager

def main() -> None:
    window: Window = Window()
    pygame.display.set_caption("Симулятор пьяного украинского лесоруба")

    TileManager.init()
    GameObject.load_textures()

    game_loop: GameLoop = GameLoop(window)
    game_loop.run()

if __name__ == '__main__':
    main()
