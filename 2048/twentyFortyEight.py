"""
Clone of 2048 game.
"""

#import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def shift_line(line):
    """
    Function that shifts non zero values to left most indices
    """
    new_line = [0] * len(line)
    non_zero_values = 0

    for value in line:
        if value > 0:
            new_line[non_zero_values] = value
            non_zero_values += 1

    return new_line


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """

    new_line = shift_line(line)

    for index, value in enumerate(new_line):
        next_value = new_line[index + 1] if index + 1 < len(new_line) else None

        if value == next_value:
            new_line[index] *= 2
            new_line[index + 1] = 0

    return shift_line(new_line)


def traverse_grid(grid_options, set_tile):
    """
    Function that iterates through the cells in a grid
    in a linear direction and returns an action (callback) performed on the values from each cell stored as list. If new values are provided (new_values), it sets these values.

    Required grid_options: {start_cell, direction, num_steps, grid}

    Both start_cell is a tuple(row, col) denoting the
    starting cell

    direction is a tuple that contains difference between
    consecutive cells in the traversal
    """
    temp_values = []

    for step in range(grid_options["num_steps"]):
        row = grid_options["start_cell"][0] + \
            step * grid_options["direction"][0]
        col = grid_options["start_cell"][1] + \
            step * grid_options["direction"][1]
        temp_values.append(grid_options["grid"][row][col])
        
    merged = merge(temp_values)
    
    has_changed = 0
    
    for step in range(grid_options["num_steps"]):
        row = grid_options["start_cell"][0] + \
            step * grid_options["direction"][0]
        col = grid_options["start_cell"][1] + \
            step * grid_options["direction"][1]
        if merged[step] != grid_options["grid"][row][col]:
            has_changed += 1
        set_tile(row, col, merged[step])

    return has_changed


def handle_values_from_traverse(values):
    """
    Merges values returned from initial traverse of grid when a move happens.
    """
    temp_values = []
    for value in values:
        temp_values.append(value)

    return merge(temp_values)


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = []
        self._initial_tiles = {
            UP: [(0, col) for col in range(self.get_grid_width())],
            DOWN: [(self.get_grid_height() - 1, col) for col in range(self.get_grid_width())],
            LEFT: [(row, 0) for row in range(self.get_grid_height())],
            RIGHT: [(row, self.get_grid_width() - 1)
                    for row in range(self.get_grid_height())]
        }
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(
            self.get_grid_width())] for dummy_row in range(self.get_grid_height())]
        self.new_tile()
        self.new_tile()

        return self._grid

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._grid)

    def get_initial_tiles(self, direction):
        """
        Get the initial tiles for moving in a certain direction.
        """

        return self._initial_tiles[direction]

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code# def run_test_suite():

        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code

        initial_tiles = self.get_initial_tiles(direction)
        rows_able_to_move = 0

        for tile in initial_tiles:
            grid_options = {
                "start_cell": tile,
                "direction": OFFSETS[direction],
                "num_steps": self.get_grid_height() if direction == UP or direction == DOWN else self.get_grid_width(),
                "grid": self._grid
            }

            rows_able_to_move += 1 if traverse_grid(
                grid_options, self.set_tile) > 0 else rows_able_to_move
            
        if rows_able_to_move > 0:
                self.new_tile()
        

    def new_tile(self):
        """
        Create a new tile iSn a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        number_choices = [2] * 9
        number_choices.append(4)
        number_to_add = random.choice(number_choices)
        empty_cells = []

        for row_index, row in enumerate(self._grid):
            for column_index, cell in enumerate(row):
                if cell == 0:
                    empty_cells.append((row_index, column_index))
        if len(empty_cells) == 0:
            print "You lose."
        cell_to_change = random.choice(empty_cells)
        self.set_tile(cell_to_change[0], cell_to_change[1], number_to_add)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]


#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
