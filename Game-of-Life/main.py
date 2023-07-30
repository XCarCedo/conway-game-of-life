import pygame

from colors import Colors
from engine import Engine
from enum import Enum


class CellStatus(Enum):
    ALIVE = 1
    DEAD = 0


class Cell:
    def __init__(self, cell_x: int, cell_y: int, status: CellStatus):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.status = status

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
                self.board[x].append(Cell(x, y, CellStatus.DEAD))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pygame.display.set_caption(str(self.clock.get_fps()))

    def draw(self):
        self.display.fill(Colors.GRAY)

        self.draw_cells()

        pygame.display.flip()

    def draw_cells(self):
        for row in self.board:
            for cell in row:
                position_on_screen = (
                    cell.cell_x * self.cell_size[0],
                    cell.cell_y * self.cell_size[1],
                )

                cell_color = {
                    CellStatus.ALIVE: Colors.BLACK,
                    CellStatus.DEAD: Colors.RAYWHITE,
                }[cell.status]

                pygame.draw.rect(
                    self.display,
                    cell_color,
                    pygame.Rect(
                        *position_on_screen,
                        self.cell_size[0] - 1,
                        self.cell_size[1] - 1,
                    ),
                )


if __name__ == "__main__":
    GameOfLife(
        screen_size=(640, 640),
        configs={
            "cell_size": (32, 32),
        },
    )
