import pygame

from pathlib import Path

from camera import Camera
from character import Player
from .level import Level


class LevelManager:
    def __init__(self, player: Player, camera: Camera) -> None:
        self.player = player
        self.camera = camera

        self.current_level: str = "home"
        self.levels: dict[str, Level] = dict()
        self.load_levels()

    def load_levels(self) -> None:
        self.levels.clear()
        path: Path = Path("../resources/data/levels/")

        for obj in path.iterdir():
            if not obj.is_file():
                continue

            if obj.suffix == ".json":
                self.levels.setdefault(
                    obj.stem,
                    Level(obj.stem, self.player, self.camera, self)
                )

        print(f"Loaded {len(self.levels)} levels")

    def update_level(self) -> None:
        level = self.levels.get(self.current_level, None)
        if level is None:
            raise ValueError(f"Level {self.current_level} does not exist!")

        level.update()

    def draw_level(self, surface: pygame.Surface) -> None:
        level = self.levels.get(self.current_level, None)
        if level is None:
            raise ValueError(f"Level {self.current_level} does not exist!")

        level.draw(surface)
