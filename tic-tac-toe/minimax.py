"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import poc_simpletest

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    result = board.check_win()

    if result != None:
        print "RESULT!"
        return SCORES[result], (-1, -1)

    cloned_board = board.clone()
    
    available_moves = cloned_board.get_empty_squares()
    
    strategy = 0
    
    for move in available_moves:
      print "No result, making move"
      cloned_board.move(move[0], move[1], player)
      next_player = provided.switch_player(player)
      score = mm_move(cloned_board, next_player)
      strategy = score[0], move
                
    return strategy


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


def test_suite():
    suite = poc_simpletest.TestSuite()

    board = provided.TTTBoard(3)
    for x_move in [(2, 0), (2, 1), (1, 2)]:
        board.move(x_move[0], x_move[1], provided.PLAYERX)
    for o_move in [(0, 0), (0, 1), (1, 1)]:
        board.move(o_move[0], o_move[1], provided.PLAYERO)
    
    print "initial board\n", board
    print mm_move(board, provided.PLAYERX)


test_suite()
