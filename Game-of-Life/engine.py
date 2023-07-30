import pygame

from abc import ABC
from abc import abstractmethod


class Engine(ABC):
    def __init__(self, screen_size=(560, 560), fps=60, configs={}) -> None:
        self.screen_size = screen_size
        self.configs = configs
        self.fps = fps

        self.init_engine()
        self.run()

    def init_engine(self):
        pygame.init()

        self.running = True
        self.display = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

    def _fps_locker(self):
        self.clock.tick(self.fps)

    @abstractmethod
    def init_game(self):
        pass

    @abstractmethod
    def check_events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def run(self):
        self.init_game()
        while self.running:
            self._fps_locker()
            self.check_events()
            self.update()
            self.draw()
