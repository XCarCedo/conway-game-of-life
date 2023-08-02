import pygame

from abc import ABC
from abc import abstractmethod


class Engine(ABC):

    """The abstract engine class that implement basic features like game loop, fps locker and etc...

    Attributes:
        clock (pygame.time.Clock): The clock object used to lock fps
        configs (dict): The configs dictionary is saved as self.configs for the game class that inherits Engine
        display (pygame.Surface): The main window display surface
        fps (int): The locked fps value
        last_tick_time (int): Processing time used in the last tick, can be used with timers
        running (bool): Determines the application is running or not, self.running=False to close
        screen_size (tuple[int,int]): The screen size
    """

    def __init__(self, screen_size=(560, 560), fps=60, configs={}) -> None:
        self.screen_size = screen_size
        self.configs = configs
        self.fps = fps
        self.last_tick_time = 0

        self.init_engine()
        self.run()

    def init_engine(self) -> None:
        """Initialize the engine and graphics libraries used"""
        pygame.init()

        self.running = True
        self.display = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

    def _fps_locker(self) -> None:
        """Locks the fps to self.fps and saves the time passed into self.last_tick_time"""
        self.last_tick_time = self.clock.tick(self.fps)

    @abstractmethod
    def init_game(self):
        """The game class that inherits can use this method to initialize the game
        This method is only called one time at the beggining of game loop before everyting else
        """
        pass

    @abstractmethod
    def check_events(self):
        """The game class that inherits can use this method to check for actions and event updates"""
        pass

    @abstractmethod
    def update(self):
        """The game class that inerhits can use this method to update the state of application
        every frame
        """
        pass

    @abstractmethod
    def draw(self):
        """The game class that inherits can use this method to draw the updates to display surface"""
        pass

    def run(self):
        """Run's the game loop"""
        self.init_game()
        while self.running:
            self._fps_locker()
            self.check_events()
            self.draw()
            self.update()
        pygame.quit()
