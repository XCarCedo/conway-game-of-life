import pygame

from colors import Colors
from engine import Engine
from enum import Enum


class CellStatus(Enum):
    ALIVE = 1
    DEAD = 0


class Cell:
    def __init__(self, status: CellStatus):
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
                self.board[x].append(Cell(CellStatus.DEAD))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pygame.display.set_caption(str(self.clock.get_fps()))

    def draw(self):
        self.display.fill(Colors.RAYWHITE)
        pygame.display.flip()

    def draw_cells(self):
        pass


if __name__ == "__main__":
    GameOfLife(
        screen_size=(640, 640),
        configs={
            "cell_size": (32, 32),
        },
    )
