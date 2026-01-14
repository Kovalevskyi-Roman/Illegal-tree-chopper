import pygame

from copy import deepcopy
from ui import Button, Label
from window import Window
from level import TileManager


class SidePanel:
    def __init__(self, game_state_manager: "GameStateManager", editor: "Editor") -> None:
        self.game_state_manager = game_state_manager
        self.editor = editor

        self.width: int = round(Window.SIZE[0] / 5.12)
        self.x = Window.SIZE[0] - self.width

        font = pygame.font.SysFont("Tahoma", 20)

        self.safe_tile_del_btn: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(self.x + 32 + TileManager.TILE_SIZE, 16, self.width - 48 - TileManager.TILE_SIZE, TileManager.TILE_SIZE),
            pygame.Surface([self.width - 48 - TileManager.TILE_SIZE, TileManager.TILE_SIZE]),
            f"Safe del: {self.editor.safe_tile_deleting}",
            font,
            "#efefef"
        )

        self.move_game_object_lbl: Label = Label(f"[M]ove: {self.editor.move_game_object}", font, "#efefef")
        self.snap_to_grid_lbl: Label = Label(f"To [G]rid: {self.editor.snap_to_grid}", font, "#efefef")

        self.new_game_object_btn: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(self.x + 16, 96 + TileManager.TILE_SIZE, self.width - 32, TileManager.TILE_SIZE),
            pygame.Surface([self.width - 32, TileManager.TILE_SIZE]),
            "New object",
            font,
            "#efefef"
        )
        self.selected_game_obj_name: Label = Label("", font, "#efefef")
        self.selected_game_obj_pos: Label = Label("", font, "#efefef")

        self.edit_game_object_btn: Button = Button(
            pygame.mouse.get_just_pressed,
            0,
            pygame.Rect(self.x + 16, 174 + TileManager.TILE_SIZE * 2, self.width - 32, TileManager.TILE_SIZE),
            pygame.Surface([self.width - 32, TileManager.TILE_SIZE]),
            "Edit data",
            font,
            "#efefef"
        )

    def update(self) -> None:
        self.move_game_object_lbl.update(f"[M]ove: {self.editor.move_game_object}")
        self.snap_to_grid_lbl.update(f"To [G]rid: {self.editor.snap_to_grid}")

        if self.safe_tile_del_btn.is_hovered():
            self.safe_tile_del_btn.texture.fill("#545454")
        else:
            self.safe_tile_del_btn.texture.fill("#323232")
        if self.safe_tile_del_btn.is_active():
            self.editor.safe_tile_deleting = not self.editor.safe_tile_deleting
            self.safe_tile_del_btn.text = f"Safe del: {self.editor.safe_tile_deleting}"
            self.safe_tile_del_btn.update_render()
            self.safe_tile_del_btn.texture.fill("#787878")

        if self.edit_game_object_btn.is_hovered():
            self.edit_game_object_btn.texture.fill("#545454")
        else:
            self.edit_game_object_btn.texture.fill("#323232")
        if self.edit_game_object_btn.is_active():
            self.game_state_manager.GAME_STATES.get(self.game_state_manager.DATA_EDITOR).init()
            self.game_state_manager.change_state(self.game_state_manager.DATA_EDITOR)

        if self.new_game_object_btn.is_hovered():
            self.new_game_object_btn.texture.fill("#545454")
        else:
            self.new_game_object_btn.texture.fill("#323232")

        if self.new_game_object_btn.is_active() and self.editor.selected_game_object == -1:
            self.editor.game_objects.append(
                {
                    "name": "null",
                    "data": {
                        "position": [0, 0]
                    }
                }
            )
            self.editor.selected_game_object = len(self.editor.game_objects) - 1
            self.editor.move_game_object = True

    def draw(self) -> None:
        pygame.draw.rect(
            Window.ui_surface, (99, 99, 99, 180), [self.x, 0, self.width, Window.SIZE[1]]
        )
        Window.ui_surface.blit(
            TileManager.tile_textures[self.editor.selected_tile],[self.x + 16, 16]
        )
        self.safe_tile_del_btn.draw(Window.ui_surface)
        self.move_game_object_lbl.draw(Window.ui_surface, [self.x + 16, 32 + TileManager.TILE_SIZE])
        self.snap_to_grid_lbl.draw(Window.ui_surface, [self.x + 16, 56 + TileManager.TILE_SIZE])
        self.new_game_object_btn.draw(Window.ui_surface)

        if self.editor.selected_game_object != -1:
            self.selected_game_obj_name.update(
                f"Obj: {self.editor.game_objects[self.editor.selected_game_object].get("name")}"
            )
            self.selected_game_obj_name.draw(
                Window.ui_surface,
                [self.x + 16, 112 + TileManager.TILE_SIZE * 2]
            )
            self.selected_game_obj_pos.update(
                f"Pos: {self.editor.game_objects[self.editor.selected_game_object].get("data").get("position")}"
            )
            self.selected_game_obj_pos.draw(
                Window.ui_surface,
                [self.x + 16, 134 + TileManager.TILE_SIZE * 2]
            )
            self.edit_game_object_btn.draw(Window.ui_surface)
