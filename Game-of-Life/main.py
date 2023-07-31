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

    def __repr__(self):
        return f"Cell({self.status})"


class GameOfLife(Engine):
    def init_game(self):
        self.cell_size = self.configs["cell_size"]
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
            if event.type == pygame.MOUSEBUTTONUP:
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

    def update(self):
        pass

    def draw(self):
        self.display.fill(Colors.GRAY)

        self.draw_cells()

        pygame.display.flip()

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


if __name__ == "__main__":
    GameOfLife(
        screen_size=(640, 640),
        configs={
            "cell_size": (32, 32),
        },
    )
