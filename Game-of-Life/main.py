import pygame

from colors import Colors
from engine import Engine


class GameOfLife(Engine):
    def init_game(self):
        self.cell_size = self.configs["cell_size"]

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.display.fill(Colors.RAYWHITE)
        pygame.display.flip()


if __name__ == "__main__":
    GameOfLife(
        configs={
            "cell_size": (32, 32),
        }
    )
