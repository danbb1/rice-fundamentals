"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided
# import poc_simpletest

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000         # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.


def mc_trial(board, player):
    """
    Takes the current board and next player to move. Plays a game by making random moves, alternating between players (starting with the next player).
    """
    next_player = player
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        next_move = random.choice(empty_squares)
        board.move(next_move[0], next_move[1], next_player)
        next_player = provided.switch_player(next_player)

    return


def mc_update_scores(scores, board, player):
    """
    Takes a grid of scores, a completed game board and which player the machine is. Scores the completed board and updates the scores grid.
    """
    result = board.check_win()

    if result == provided.DRAW:
        return

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            square = board.square(row, col)
            if square == provided.EMPTY:
                continue
            if square == result:
    print new_game.time_until(300)
                scores[row][col] = scores[row][col] + \
                    SCORE_CURRENT if square == player else scores[row][col] + SCORE_OTHER
            else:
                scores[row][col] = scores[row][col] - \
                    SCORE_CURRENT if square == player else scores[row][col] - SCORE_OTHER


def get_best_move(board, scores):
    """
    Takes the current board and a grid of scores. Finds all empty squares with the maximum score and randomly returns one of these.
    """
    empty_squares = board.get_empty_squares()
    max_squares = []
    max_value = 0

    for square in empty_squares:
        if len(max_squares) == 0:
            max_squares.append(square)
            max_value = scores[square[0]][square[1]]
            continue

        if scores[square[0]][square[1]] < max_value:
            continue
        elif scores[square[0]][square[1]] > max_value:
            max_squares = [square]
            max_value = scores[square[0]][square[1]]
        elif scores[square[0]][square[1]] == max_value:
            max_squares.append(square)

    return random.choice(max_squares)


def mc_move(board, player, trials):
    """
    Takes the current board, which player the machine is and the amount of trials to run. Returns the best move for the machine player.
    """
    scores = [[0 for dummy_col in range(board.get_dim())]
              for dummy_row in range(board.get_dim())]

    for dummy_trial in range(trials):
        cloned_board = board.clone()
        mc_trial(cloned_board, player)
        mc_update_scores(scores, cloned_board, player)

    return get_best_move(board, scores)


# def run_tests():
#     suite = poc_simpletest.TestSuite()

#     board = provided.TTTBoard(3)
#     mc_trial(board, provided.PLAYERX)
#     suite.run_test(board.check_win != None or len(
#         board.get_empty_squares()) == 0, True, "mc_trial plays a game to completion")
#     board = provided.TTTBoard(3)
#     mc_move(board, provided.PLAYERX, 1)

#     suite.report_results()


# run_tests()
# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, mc_move, NTRIALS, False)
