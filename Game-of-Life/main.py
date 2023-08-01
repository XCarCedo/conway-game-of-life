import argparse
import json
import math
import pygame
import tkinter
import tkinter.filedialog

from colors import Colors
from engine import Engine
from enum import Enum


class CellStatus(Enum):
    ALIVE = 1
    DEAD = 0


class Cell:
    def __init__(
        self,
        cell_x: int,
        cell_y: int,
        cell_size: tuple[int, int],
        status: CellStatus,
        game,
    ):
        self.game = game
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.status = status
        self.cell_size = cell_size
        self.rect = pygame.Rect(
            cell_x * cell_size[0],
            cell_y * cell_size[1],
            cell_size[0] - 1,
            cell_size[0] - 1,
        )

    def toggle(self):
        self.status = {
            CellStatus.ALIVE: CellStatus.DEAD,
            CellStatus.DEAD: CellStatus.ALIVE,
        }[self.status]

    def copy(self):
        return Cell(self.cell_x, self.cell_y, self.cell_size, self.status, self.game)

    def get_neighbors_count(self) -> int:
        neighbor_count = 0

        # Top
        neighbor_count += self.game.get_cell_status(self.cell_x - 1, self.cell_y)
        # Top-left
        neighbor_count += self.game.get_cell_status(self.cell_x - 1, self.cell_y - 1)
        # Top-right
        neighbor_count += self.game.get_cell_status(self.cell_x - 1, self.cell_y + 1)
        # Left
        neighbor_count += self.game.get_cell_status(self.cell_x, self.cell_y - 1)
        # Right
        neighbor_count += self.game.get_cell_status(self.cell_x, self.cell_y + 1)
        # Bottom
        neighbor_count += self.game.get_cell_status(self.cell_x + 1, self.cell_y)
        # Bottom-left
        neighbor_count += self.game.get_cell_status(self.cell_x + 1, self.cell_y - 1)
        # Bottom-right
        neighbor_count += self.game.get_cell_status(self.cell_x + 1, self.cell_y + 1)

        return neighbor_count

    def __repr__(self):
        return f"Cell({self.status})"


class GameOfLife(Engine):
    def init_game(self):
        self.cell_size = self.configs["cell_size"]
        self.evoulate_timer_ms = self.configs["evoulate_timer_ms"]
        self.since_last_evoulate = 0
        self.running_evoulation = False
        self.last_changed_cell = None

        if "loaded_board" in self.configs:
            self.board = self.get_loadable_board(self.configs["loaded_board"])
        else:
            self.board = []
            self.init_board()

    def init_board(self):
        for x in range(self.screen_size[0] // self.cell_size[0]):
            self.board.append([])
            for y in range(self.screen_size[1] // self.cell_size[1]):
                self.board[x].append(Cell(x, y, self.cell_size, CellStatus.DEAD, self))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.running_evoulation = not self.running_evoulation
            elif (
                event.type == pygame.KEYUP
                and event.key == pygame.K_c
                and not self.running_evoulation
            ):
                self.clear_board()

    def update(self):
        pygame.display.set_caption(
            f"Conway's Game Of Life | "
            + f"{'Evoulating' if self.running_evoulation else 'Paused'} | "
            + f"FPS: {round(self.clock.get_fps())}"
        )
        if self.running_evoulation:
            self.since_last_evoulate += self.last_tick_time
            if self.since_last_evoulate >= self.evoulate_timer_ms:
                self.since_last_evoulate = 0
                self.evoulate()
        else:
            lmb_pressed = pygame.mouse.get_pressed()[0]
            if lmb_pressed:
                mouse_pos = pygame.mouse.get_pos()
                clicked_cell_pos = (
                    math.floor(mouse_pos[0] / self.cell_size[0]),
                    math.floor(mouse_pos[1] / self.cell_size[1]),
                )
                if self.last_changed_cell != clicked_cell_pos:
                    clicked_cell = self.board[clicked_cell_pos[0]][clicked_cell_pos[1]]
                    clicked_cell.toggle()
                    self.last_changed_cell = clicked_cell_pos

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RCTRL] or pressed_keys[pygame.K_LCTRL]:
                if pressed_keys[pygame.K_s]:
                    self.save_state_file()
                elif pressed_keys[pygame.K_r]:
                    self.load_state_file()

    def draw(self):
        self.display.fill(Colors.GRAY)

        self.draw_cells()

        pygame.display.flip()

    def get_saveable_board(self):
        return [
            [{CellStatus.DEAD: 0, CellStatus.ALIVE: 1}[cell.status] for cell in row]
            for row in self.board
        ]

    def get_loadable_board(self, config_json):
        new_board = []
        for x, row in enumerate(config_json):
            new_board.append([])
            for y, cell in enumerate(row):
                new_board[x].append(
                    Cell(
                        x,
                        y,
                        self.cell_size,
                        {0: CellStatus.DEAD, 1: CellStatus.ALIVE}[cell],
                        self,
                    )
                )
        return new_board

    def unpack_state(self, config_json):
        self.running = False
        GameOfLife(
            config_json["screen_size"],
            self.fps,
            {
                "cell_size": self.cell_size,
                "evoulate_timer_ms": self.evoulate_timer_ms,
                "loaded_board": config_json["board"],
            },
        )

    def save_state_file(self):
        top = tkinter.Tk()
        top.withdraw()
        state_file_path = tkinter.filedialog.asksaveasfilename(
            parent=top, filetypes=(("Game of Life State", ".gols"),)
        )
        top.destroy()

        saved_state = {
            "board": self.get_saveable_board(),
            "cell_size": self.cell_size,
            "screen_size": self.screen_size,
        }
        with open(state_file_path, mode="w") as save_state_file:
            json.dump(saved_state, save_state_file)

    def load_state_file(self):
        top = tkinter.Tk()
        top.withdraw()
        state_file_path = tkinter.filedialog.askopenfilename(
            parent=top, filetypes=(("Game of Life State", ".gols"),)
        )
        top.destroy()

        with open(state_file_path, mode="r") as load_state_file:
            saved_state = json.load(load_state_file)
            self.unpack_state(saved_state)

    def clear_board(self):
        for row in self.board:
            for cell in row:
                cell.status = CellStatus.DEAD

    def get_cell_status(self, cell_x, cell_y):
        try:
            return {CellStatus.ALIVE: 1, CellStatus.DEAD: 0}[
                self.board[cell_x][cell_y].status
            ]
        except IndexError:
            return 0

    def draw_cells(self):
        for row in self.board:
            for cell in row:
                cell_color = {
                    CellStatus.ALIVE: Colors.BLACK,
                    CellStatus.DEAD: Colors.RAYWHITE,
                }[cell.status]

                pygame.draw.rect(
                    self.display,
                    cell_color,
                    cell.rect,
                )

    def evoulate(self):
        next_level_board = [[cell.copy() for cell in row] for row in self.board]
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                neighbor_count = cell.get_neighbors_count()
                if cell.status == CellStatus.ALIVE and (not neighbor_count in (2, 3)):
                    next_level_board[x][y].toggle()
                elif cell.status == CellStatus.DEAD and neighbor_count in (3,):
                    next_level_board[x][y].toggle()
        self.board = next_level_board


def get_args_config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conway's Game of Life")

    parser.add_argument(
        "-f",
        "--fps",
        default=0,
        help="The locked framerate of display window (0 for no limits)",
    )
    parser.add_argument(
        "-s", "--screen-size", default="640x640", help="The size of display screen"
    )
    parser.add_argument(
        "-etm",
        "--evoulate-timer-ms",
        default=250,
        help="The time between each evoulate progress",
    )
    parser.add_argument(
        "-cs",
        "--cell-size",
        default="16x16",
        help="The size of each cell (automatically divides the display based on this value)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args_config()
    GameOfLife(
        screen_size=tuple(map(int, args.screen_size.lower().split("x"))),
        fps=int(args.fps),
        configs={
            "cell_size": tuple(map(int, args.cell_size.lower().split("x"))),
            "evoulate_timer_ms": int(args.evoulate_timer_ms),
        },
    )
