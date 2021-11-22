# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
          '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [
                          pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class


class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        _str = "Hand contains: "
        for card in self.cards:
            _str = _str + card.get_suit() + card.get_rank() + ", "
        return _str + "value is " + str(self.get_value())

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        total_value = 0

        for card in self.cards:
            card_value = VALUES.get(card.get_rank())
            total_value += card_value

        for card in self.cards:
            if card.get_rank() == "A" and total_value + 10 <= 21:
                total_value += 10

        return total_value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for count, card in enumerate(self.cards):
            card.draw(canvas, [pos[0] + (count * 72) + (count * 2), pos[1]])

# define deck class


class Deck:
    def __init__(self):
        self.cards = []

        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        top_card = self.cards[0]
        self.cards.pop(0)
        return top_card

    def __str__(self):
        str = "Deck contains: "
        if len(self.cards) > 0:
            for card in self.cards:
                str = str + card.get_suit() + card.get_rank() + ", "
        else:
            str = "Deck contains: None"
        return str


# define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score

    if in_play == True:
        outcome = "You lose."
        score -= 1

    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    in_play = True
    outcome = ""


def hit():
    global player_hand, deck, outcome, score, in_play
    # if the hand is in play, hit the player
    if in_play == True and player_hand.get_value() < 21:
        player_hand.add_card(deck.deal_card())

        if player_hand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "You have busted."
    # if busted, assign a message to outcome, update in_play and score


def stand():
    global player_hand, in_play, score, outcome

    if player_hand.get_value() > 21:
        outcome = "You have ALREADY busted. Can't hit. Deal to play again."
        return

    in_play = False

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())

        # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() > 21:
        score += 1
        outcome = "Dealer busted."
    elif dealer_hand.get_value() > player_hand.get_value() or dealer_hand.get_value() == player_hand.get_value():
        in_play = False
        score -= 1
        outcome = "Dealer wins."
    else:
        score += 1
        in_play = False
        outcome = "You win."
# draw handler


def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand, outcome, score
    player_hand.draw(canvas, [100, 350])
    dealer_hand.draw(canvas, [100, 150])
    canvas.draw_text(outcome, [100, 500], 32, "Black")
    canvas.draw_text("Score: " + str(score), [50, 50], 32, "Black")

    if in_play == True:
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [
                          136, 198], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
