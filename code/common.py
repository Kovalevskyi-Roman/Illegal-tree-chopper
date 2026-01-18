import pygame

TILE_SIZE: int = 48
GAME_OBJECT_SIZE: int = 48
ITEM_SIZE: int = 48
CURSOR_BLINK_TIME: float = 0.45

FONT_18: pygame.Font = pygame.font.SysFont("Tahoma", 18)
FONT_20: pygame.Font = pygame.font.SysFont("Tahoma", 20)
FONT_24: pygame.Font = pygame.font.SysFont("Tahoma", 24)
FONT_30: pygame.Font = pygame.font.SysFont("Tahoma", 30)

game_time: float = 12 * 60  # seconds
player_money: int = 0
