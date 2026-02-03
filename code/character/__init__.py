
from typing import Any
from .character import Character
from .player import Player
from .chest import Chest
from .police_man import PoliceMan

def character_factory(data: dict[str, Any]) -> Character:
    name = data.get("name")

    match name:
        case "character":
            return Character(data)

        case "player":
            return Player(data)

        case "chest":
            return Chest(data)

        case "police_man":
            return PoliceMan(data)

        case _:
            raise ValueError(f"Unknown character: {name}")
