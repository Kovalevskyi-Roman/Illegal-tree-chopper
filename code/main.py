import pygame

pygame.init()

from window import Window
from game_loop import GameLoop
from level import TileManager
from game_object import GameObject
from tool import Tool
from item import Item

def main() -> None:
    window: Window = Window()
    pygame.display.set_caption("Симулятор нелегального лесоруба")

    TileManager.init()
    GameObject.load_textures()
    Tool.init()
    Item.init()

    GameLoop(window).run()

if __name__ == '__main__':
    main()
