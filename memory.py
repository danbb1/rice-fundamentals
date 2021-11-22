# implementation of card game - Memory

import simplegui
import random

SINGLE_LIST = [i + 1 for i in range(8)]
TILE_WIDTH = 50
TILE_HEIGHT = 100
exposed_cards_this_turn = []
turns = 0

#classes

class Tile:
  def __init__(self, number, exp, location):
      self.number = number
      self.exposed = exp
      self.location = location

  def __str__(self):
    return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)

  def get_number(self):
    return self.number
  
  def is_exposed(self):
    return self.exposed
  
  def expose_tile(self):
    self.exposed = True
  
  def hide_tile(self):
    self.exposed = False

  def draw_tile(self, canvas):
    if self.exposed == True:
      canvas.draw_text(str(self.number), (self.location[0] + TILE_WIDTH / 3, TILE_HEIGHT / 2 + 12), 32, "White")
    else:
      canvas.draw_polygon([[self.location[0], 0], [(self.location[0] + TILE_WIDTH), 0], [(self.location[0] + TILE_WIDTH), TILE_HEIGHT], [self.location[0], 100]], 1, "Black", "Green")

  def is_selected(self, pos):
    


my_tile = Tile(3)
your_tile = Tile(4)

# helper function to initialize globals
def new_game():
    global game_cards, exposed
    game_cards = list(SINGLE_LIST)
    game_cards.extend(list(SINGLE_LIST))
    random.shuffle(game_cards)
    exposed = [False for card in range(len(game_cards))]

def check_match(exposed_cards):
  if game_cards[exposed_cards[0]] == game_cards[exposed_cards[1]]:
    return
  exposed[exposed_cards[0]], exposed[exposed_cards[1]] = False, False

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed_cards_this_turn, turns
    clicked_card = pos[0] // 50
    if exposed[clicked_card] == True:
      return
    exposed_cards_this_turn.append(clicked_card)
    exposed[clicked_card] = True

    if len(exposed_cards_this_turn) == 2:
      turns += 1
      
    if len(exposed_cards_this_turn) == 3:
      check_match(exposed_cards_this_turn)
      exposed_cards_this_turn.pop(0)
      exposed_cards_this_turn.pop(0)

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global game_cards, turns
    for count, value in enumerate(game_cards):
      if exposed[count] == False:
        canvas.draw_polygon([[count * 50, 0], [(count + 1) * 50, 0], [(count + 1) * 50, 100], [count * 50, 100]], 1, "Black", "Green")
      else :
        canvas.draw_text(str(value), ((50 * count) + 12.5, HEIGHT / 2 + 12), 32, "White")
    canvas.draw_text("Turns: " + str(turns), [25, 25], 18, "White")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric