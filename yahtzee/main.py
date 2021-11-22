"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import poc_simpletest
import codeskulptor
codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def check_three_kind(hand):
    """
    Checks three of a kind
    """
    for die in hand:
        if hand.count(die) == 3:
            return (True, die)

    return (False, None)


def check_house(hand, three_of_kind_die):
    """
    Checks house, takes full hand and the three of kind value
    """
    remaining_two_dies = [
        r_die for r_die in hand if r_die != three_of_kind_die]

    return remaining_two_dies[0] == remaining_two_dies[1]


def check_four_kind(hand):
    """
    Checks four of a kind
    """
    for die in hand:
        if hand.count(die) == 4:
            return (True, die)

    return (False, None)


def score(hand, already_played):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    Already played is a list of squares already played to be ignored in highest score calculation

    hand: full yahtzee hand

    Returns an integer score 
    """
    possible_scores = {
        1: hand.count(1) * 1,
        2: hand.count(2) * 2,
        3: hand.count(3) * 3,
        4: hand.count(4) * 4,
        5: hand.count(5) * 5,
        6: hand.count(6) * 6,
        "three_of_kind": 0,
        "four_of_kind": 0,
        "full_house": 0,
        "sm_straight": 0,
        "lg_straight": 0,
        "yahtzee": 0,
        "chance": sum(hand),
    }

    # check 3 of a kind
    three_kind_res = check_three_kind(hand)

    if three_kind_res[0] == True:
        possible_scores.update({"three_of_kind": sum(hand)})
        if check_house(hand, three_kind_res[1]):
            possible_scores.update({"full_house": 25})

    # check four of kind
    four_kind_res = check_four_kind(hand)

    if four_kind_res[0] == True:
        possible_scores.update({"four_of_kind": sum(hand)})

    # check straights
    sorted_hand = sorted(hand)
    consecutive_dies = 1
    for index, sorted_die in enumerate(sorted_hand):
        if index == len(sorted_hand) - 1:
            break
        if sorted_hand[index + 1] - sorted_die == 1:
            consecutive_dies += 1
            if consecutive_dies == 4:
                possible_scores.update({"sm_straight": 30})
                if consecutive_dies == 5:
                    possible_scores.update({"lg_straight": 40})
        else:
            break

    # check yahtzee
    hand_set = set(hand)
    if len(hand_set) == 1:
        possible_scores.update({"yahtzee": 50})

    for key in already_played:
        possible_scores.update({key: 0})

    max_key = max(possible_scores, key=possible_scores.get)
    return possible_scores[max_key]


def expected_value(held_dice, num_die_sides, num_free_dice, already_played, rolls_left):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    possible_rolls = gen_all_sequences(
        list(range(1, num_die_sides + 1)), num_free_dice)

    exp_value = 0.0
    for dummy_index in range(rolls_left):
        for roll in possible_rolls:
            holdscore = score(held_dice + roll, already_played)
            exp_value += float(holdscore) / float(len(possible_rolls) * rolls_left)

    return exp_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    possible_holds = set([(), hand])

    # possible holds generated recursively by removing the current die from the recursive call.

    for die in hand:
        cloned_hand = list(hand)
        cloned_hand.remove(die)
        recursive = gen_all_holds(tuple(cloned_hand))
        possible_holds.update(recursive)
    sorted_possible_holds = [tuple(sorted(hold)) for hold in possible_holds]

    return set(sorted_possible_holds)


def strategy(hand, num_die_sides, already_played, rolls_left):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    best_move = (0.0, ())
    possible_holds = gen_all_holds(hand)

    for held_dice in possible_holds:
        hold_ev = expected_value(
            held_dice, num_die_sides, len(hand) - len(held_dice), already_played, rolls_left)
        if hold_ev > best_move[0]:
            best_move = (hold_ev, held_dice)

    return best_move

# def run_example():
#     """
#     Compute the dice to hold and expected score for an example hand
#     """
#     num_die_sides = 6
#     hand = (1, 1, 1, 5, 6)
#     hand_score, hold = strategy(hand, num_die_sides)
#     print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


# run_example()


# def run_tests():
#     suite = poc_simpletest.TestSuite()

#     # hand = (1, 2, 3, 4, 5)
#     # suite.run_test(score(hand), 5, "Score test #1")
#     # hand = (1, 1, 1, 1, 1)
#     # suite.run_test(score(hand), 5, "Score test #2")
#     # hand = (6, 6, 6, 6, 6)
#     # suite.run_test(score(hand), 30, "Score test #3")
#     # hand = (2, 2, 2, 6, 6)
#     # suite.run_test(score(hand), 12, "Score test #1")
#     # hand = (5, 4, 5, 4, 4)
#     # suite.run_test(score(hand), 12, "Score test #1")
#     # suite.run_test(expected_value((1, 1), 3, 1), 8 / 3, "EV test #1")
#     # suite.run_test(expected_value((1, 2), 3, 1), 3, "EV test #2")
#     # suite.run_test(expected_value((1,), 3, 2), 3, "EV test #3")
#     # suite.run_test(expected_value((1, 2, 3), 6, 2), float(210 / 36), "EV test #3")
#     # suite.run_test(expected_value((1, 1, 1), 6, 1), float(25 / 6), "EV test #4")
#     suite.run_test(expected_value((6, 6, 6), 6, 2), True, "EV test 5")

#     suite.report_results()


# run_tests()


#import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
