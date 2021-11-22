"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """

    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]

    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = list(configuration)

    def __str__(self):
        """
        Return string representation for Mancala board
        """

        temp = list(self._board)
        temp.reverse()

        return str(temp)

    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        removed_house = list(self._board)
        removed_house.pop(0)
        for house_num in removed_house:
            if house_num != 0:
                return False

        return True

    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        if house_num == 0 or self.get_num_seeds(house_num) != house_num:
            return False

        return True

    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):
            index = 0
            self._board[house_num] = 0
            while index < house_num:
                self._board[index] += 1
                index += 1

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """

        return next((house_num for house_num, dummy_house_value in enumerate(self._board) if self.is_legal_move(house_num) == True), 0)

    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: After each move, move the seeds in the house closest to the store when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        copied_board = SolitaireMancala()
        copied_board.set_board(self._board)
        moves = []
        next_move = copied_board.choose_move()
        while next_move != 0:
            copied_board.apply_move(next_move)
            moves.append(next_move)
            next_move = copied_board.choose_move()

        return moves


# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """

    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"

    config1 = [0, 0, 1, 1, 3, 5, 0]
    config2 = [0, 0, 0, 1, 2, 2, 0]
    config3 = [0, 0, 2, 1, 3, 5, 0]
    config4 = [10, 0, 0, 0, 0, 0, 0]
    my_game.set_board(config1)

    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]
    print
    print "Testing is_legal_move position 5 - Computed:", my_game.is_legal_move(5), "Expected: True"
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(4), "Expected: False"
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(0), "Expected: False"
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(1), "Expected: False"
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(2), "Expected: False"
    print
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected: 5"
    print "Testing apply_move - Computed:"
    my_game.apply_move(5)
    print str(my_game), "Expected: ", str([0, 0, 4, 2, 2, 1, 1])
    print "Testing apply_move - Computed:"
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected: 1"
    my_game.apply_move(1)
    print str(my_game), "Expected: ", str([0, 0, 4, 2, 2, 0, 2])
    print "Testing apply_move - Computed:"
    my_game.apply_move(2)
    print str(my_game), "Expected: ", str([0, 0, 4, 2, 0, 1, 3])
    print "Testing apply_move - Computed:"
    my_game.apply_move(4)
    print str(my_game), "Expected: ", str([0, 0, 0, 3, 1, 2, 4])
    print "Testing apply_move - Computed:"
    my_game.apply_move(5)
    print str(my_game), "Expected: ", str([0, 0, 0, 3, 1, 2, 4])
    print "Testing apply_move - Computed:"
    my_game.apply_move(4)
    print str(my_game), "Expected: ", str([0, 0, 0, 3, 1, 2, 4])
    my_game.set_board(config2)
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected: 0"
    my_game.set_board(config3)
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected: 2"
    my_game.set_board(config4)
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected: True"
    my_game.set_board(config1)
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected: False"
    my_game.set_board(config2)
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected: False"
    my_game.set_board(config1)
    print "Testing plan moves - Computed: ", my_game.plan_moves(), "Expected: [5, 1, 2, 1, 4, 1, 3, 1, 2, 1"


    # add more tests here
test_mancala()


# import poc_mancala_gui
# poc_mancala_gui.run_gui(SolitaireMancala())
