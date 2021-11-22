# template for "Stopwatch: The Game"
import simplegui
# define global variables
is_stopped = True
counter, score, attempts = 0, 0 , 0



# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    milliseconds = t % 10
    seconds = (t // 10) % 60
    minutes = (t / 10) // 60
    
    return str(minutes) + ":" + ("0" if seconds < 10 else "") + str(seconds) + "." + str(milliseconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global is_stopped
    is_stopped = False
    timer.start()

def stop_timer():
    global is_stopped, score, attempts
    timer.stop()
    if is_stopped == True:
        return
    elif counter % 10 == 0:
        score += 1
        attempts += 1
    else:
        attempts += 1
    
    is_stopped = True


def reset_timer():
    global counter, attempts, score
    counter, attempts, score = 0, 0, 0
# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1

timer = simplegui.create_timer(100, tick)

# define draw handler
def draw_handler(canvas):
    global score
    global attempts
    canvas.draw_text(format(counter), [175, 150], 48, "White")
    canvas.draw_text(str(score) + "/" + str(attempts), [450, 25], 24, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 500, 300)
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_timer)
frame.add_button("Stop", stop_timer)
frame.add_button("Reset", reset_timer)

# register event handlers

# start frame
frame.start()

# Please remember to review the grading rubric
