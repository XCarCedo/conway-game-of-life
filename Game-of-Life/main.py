import copy
import math
import pygame

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
        self.board = []
        self.since_last_evoulate = 0
        self.running_evoulation = False

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
            if event.type == pygame.MOUSEBUTTONUP and not self.running_evoulation:
                lmb_pressed = event.button == 1
                if not lmb_pressed:
                    continue
                mouse_pos = pygame.mouse.get_pos()
                clicked_cell_pos = (
                    math.floor(mouse_pos[0] / self.cell_size[0]),
                    math.floor(mouse_pos[1] / self.cell_size[1]),
                )

                clicked_cell = self.board[clicked_cell_pos[0]][clicked_cell_pos[1]]
                clicked_cell.toggle()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.running_evoulation = not self.running_evoulation

    def update(self):
        if self.running_evoulation:
            self.since_last_evoulate += self.last_tick_time
            if self.since_last_evoulate >= self.evoulate_timer_ms:
                self.since_last_evoulate = 0
                self.evoulate()

    def draw(self):
        self.display.fill(Colors.GRAY)

        self.draw_cells()

        pygame.display.flip()

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


if __name__ == "__main__":
    GameOfLife(
        screen_size=(640, 640),
        configs={"cell_size": (32, 32), "evoulate_timer_ms": 250},
    )
