"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui
#import poc_simpletest


# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list, self._zombie_list = list([]), list([])

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        height = self.get_grid_height()
        width = self.get_grid_width()

        visited = poc_grid.Grid(height, width)
        distance_field = [
            [height * width for dummy_col in range(width)] for dummy_row in range(height)]

        boundary = poc_queue.Queue()

        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        else:
            for human in self.humans():
                boundary.enqueue(human)

        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            # continue if cell already visited
            if visited.is_empty(current_cell[0], current_cell[1]) == True:
                distance_field[current_cell[0]][current_cell[1]] = 0

            visited.set_full(current_cell[0], current_cell[1])

            for neighbor_cell in visited.four_neighbors(current_cell[0], current_cell[1]):
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]) and self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)

                    distance_field[neighbor_cell[0]][neighbor_cell[1]
                                                     ] = distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index, human in enumerate(self.humans()):
            possible_moves = self.eight_neighbors(human[0], human[1])
            best_moves = []

            for possible_move in possible_moves:
                pos_row = possible_move[0]
                pos_col = possible_move[1]
                # continue if obstacle
                if self.is_empty(pos_row, pos_col) == False or zombie_distance_field[pos_row][pos_col] == 0:
                    continue
                # if best moves empty, add move and continue
                if len(best_moves) == 0:
                    best_moves.append(possible_move)
                    continue
                best_row = best_moves[0][0]
                best_col = best_moves[0][1]
                if zombie_distance_field[pos_row][pos_col] == zombie_distance_field[best_row][best_col]:
                    best_moves.append(possible_move)
                elif zombie_distance_field[pos_row][pos_col] > zombie_distance_field[best_row][best_col]:
                    best_moves = [possible_move]

            chosen_move = random.choice(best_moves) if len(best_moves) > 0 else None

            self._human_list[index] = (chosen_move[0], chosen_move[1]) if chosen_move != None else self._human_list[index]

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for index, zombie in enumerate(self.zombies()):
            possible_moves = self.four_neighbors(zombie[0], zombie[1])
            best_moves = []

            for possible_move in possible_moves:
                pos_row = possible_move[0]
                pos_col = possible_move[1]
                # continue if obstacle
                if self.is_empty(pos_row, pos_col) == False or human_distance_field[zombie[0]][zombie[1]] == 0:
                    continue
                # if best moves empty, add move and continue
                if len(best_moves) == 0:
                    best_moves.append(possible_move)
                    continue

                best_row = best_moves[0][0]
                best_col = best_moves[0][1]
                if human_distance_field[pos_row][pos_col] == human_distance_field[best_row][best_col]:
                    best_moves.append(possible_move)
                elif human_distance_field[pos_row][pos_col] < human_distance_field[best_row][best_col]:
                    best_moves = [possible_move]

            chosen_move = random.choice(best_moves) if len(best_moves) > 0 else None

            self._zombie_list[index] = (chosen_move[0], chosen_move[1]) if chosen_move != None else self._zombie_list[index]

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))


# def all_empty(grid):
#     """
#     Helper for testing. Checks if all cells empty.
#     """
#     for row in range(grid.get_grid_height()):
#         for col in range(grid.get_grid_width()):
#             if grid.is_empty(row, col) == False:
#                 return False

#     return True


# def apocalypse_test_suite():
#     suite = poc_simpletest.TestSuite()

#     print "Running apocalypse test suite"

#     new_game = Apocalypse(10, 10, obstacle_list=[(0, 1), (5, 4), (6, 3)], human_list=[
#                           (2, 3), (3, 7)], zombie_list=[((8, 2))])

#     suite.run_test(all_empty(new_game), False, "Test #0")
#     suite.run_test(new_game.is_empty(0, 1), False, "Test #1")
#     suite.run_test(new_game.is_empty(5, 4), False, "Test #2")
#     suite.run_test(new_game.is_empty(6, 3), False, "Test #3")
#     suite.run_test(new_game.num_humans(), 2, "Test #4")
#     suite.run_test(new_game.num_zombies(), 1, "Test #5")
#     new_game.clear()
#     suite.run_test(all_empty(new_game), True, "Test #6")
#     suite.run_test(new_game.num_zombies(), 0, "Test #7")
#     suite.run_test(new_game.num_humans(), 0, "Test #8")
#     new_game.add_zombie(4, 5)
#     suite.run_test(new_game.num_zombies(), 1, "Test #9")
#     new_game.add_zombie(5, 7)
#     new_game.add_zombie(3, 5)
#     suite.run_test([zombie for zombie in new_game.zombies()],
#                    [(4, 5), (5, 7), (3, 5)], "Test #10")
#     new_game.add_human(1, 2)
#     new_game.add_human(7, 8)
#     new_game.add_human(6, 0)
#     suite.run_test(new_game.num_humans(), 3, "Test #11")
#     suite.run_test([human for human in new_game.humans()],
#                    [(1, 2), (7, 8), (6, 0)], "Test #12")

#     smaller_game = Apocalypse(
#         2, 2, obstacle_list=[(1, 1)], zombie_list=[(0, 0)])

#     suite.run_test(smaller_game.compute_distance_field(
#         ZOMBIE), [[0, 1], [1, 4]])
      
#     obj = Apocalypse(3, 3, [], [(1, 1)], [(1, 1)])
#     print obj
#     dist = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
#     obj.move_zombies(dist)
#     for zombie in obj.zombies():
#       print zombie

#     suite.report_results()


# apocalypse_test_suite()
