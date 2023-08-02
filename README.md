
# Conway's Game of Life

A simple implemention of conway Game of Life in python and pygame



## Installation

First you need to clone the project:
```bash
git clone https://github.com/XCarCedo/conway-game-of-life/
cd conway-game-of-life
```

Install the requirements:
```bash
pip install -r requirements.txt
```

Then run main.py
```bash
python main.py
```
    
## Features

- Toggle running process by pressing space
- Clear the board by pressing c
- Save/load your board state by ctrl+s/ctrl+running
- Pass command line arguments to customize the board and other things



## Command-line Arguments
```bash
Conway's Game of Life

options:
  -h, --help            show this help message and exit
  -f FPS, --fps FPS     The locked framerate of display window (0 for no limits)
  -s SCREEN_SIZE, --screen-size SCREEN_SIZE
                        The size of display screen
  -etm EVOULATE_TIMER_MS, --evoulate-timer-ms EVOULATE_TIMER_MS
                        The time between each evoulate progress
  -cs CELL_SIZE, --cell-size CELL_SIZE
                        The size of each cell (automatically divides the display based on this value)
```
## Known Bugs and Issues
- The program memory usage goes up about 2-5mb every time loading a new state by ctrl+r and this keeps adding up until the program closed
- Edges don't work correctly always there's some random cells appear to be alive sometimes

## Contributing

This project isn't perfect there are still problems that i'm aware so Issues/PR are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.