# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
HALF_PAD_WIDTH = PAD_WIDTH / 2
PAD_HEIGHT = 80
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
INITIAL_PAD_POS = [(HEIGHT / 2) - HALF_PAD_HEIGHT, (HEIGHT / 2) + HALF_PAD_HEIGHT]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]

    random_horizontal = random.randrange(2, 6)
    
    random_vertical = random.randrange(-2, 2)
    random_vertical = random_vertical + 1 if random_vertical == 0 else random_vertical

    ball_vel = [-(random_horizontal), random_vertical] if direction == "left" else [random_horizontal, random_vertical]

    print (ball_vel)

# define event handlers
def new_game():
    global pad1_vertical, pad2_vertical, pad1_vel, pad2_vel, DIRECTION  # these are numbers

    global score1, score2  # these are ints
    pad1_vertical, pad2_vertical = list(INITIAL_PAD_POS), list(INITIAL_PAD_POS)
    pad1_vel, pad2_vel, score1, score2 = 0, 0, 0, 0 
    spawn_ball("left")

def is_colliding(ball_pos, paddle_pos):
    pad_top = paddle_pos[0]
    pad_bottom = paddle_pos[1]
    ball_top = ball_pos[1] - BALL_RADIUS
    ball_bottom = ball_pos[1] + BALL_RADIUS

    if pad_top < ball_bottom and pad_bottom > ball_top:
      return True
    else:
      return False

def draw(canvas):
    global score1, score2, pad1_vertical, pad2_vertical, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # reflect off vertical boundary
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
      ball_vel[1] = - ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    if pad1_vertical[1] + pad1_vel < HEIGHT and pad1_vertical[0] + pad1_vel > 0: 
      pad1_vertical[0] += pad1_vel
      pad1_vertical[1] += pad1_vel
    if pad2_vertical[1] + pad2_vel < HEIGHT and pad2_vertical[0] + pad2_vel > 0: 
      pad2_vertical[0] += pad2_vel
      pad2_vertical[1] += pad2_vel
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, pad1_vertical[0]], [HALF_PAD_WIDTH, pad1_vertical[1]], PAD_WIDTH, "White")

    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, pad2_vertical[0]], [WIDTH - HALF_PAD_WIDTH, pad2_vertical[1]], PAD_WIDTH, "White")

    # determine whether paddle and ball collide    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
      if is_colliding(ball_pos, pad1_vertical) == True:
        ball_vel[0] = - ball_vel[0] * 1.1
      else:
        score2 += 1
        spawn_ball("right")
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
      if is_colliding(ball_pos, pad2_vertical) == True:
        ball_vel[0] = - ball_vel[0] * 1.1
      else:
        score1 += 1
        spawn_ball("left")
      
    # draw scores
    canvas.draw_text(str(score1), [(WIDTH / 4), 100], 32, "White")
    canvas.draw_text(str(score2), [3 * (WIDTH / 4), 100], 32, "White")

def keydown(key):
    global pad1_vel, pad2_vel
    if key == simplegui.KEY_MAP["w"]:
      pad1_vel = -2
    elif key == simplegui.KEY_MAP["s"]:
      pad1_vel = 2
    elif key == simplegui.KEY_MAP["up"]:
      pad2_vel = -2
    elif key == simplegui.KEY_MAP["down"]:
      pad2_vel = 2

def keyup(key):
    global pad1_vel, pad2_vel

    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
      pad1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
      pad2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("New Game", new_game)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
