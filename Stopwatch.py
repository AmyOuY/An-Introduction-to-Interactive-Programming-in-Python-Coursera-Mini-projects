# "Stopwatch: The Game"


import simplegui

# define global variables
t = 0
t_str = "0:00.0"
x = 0
y = 0
count_str = "0/0" 
timer_run = False



# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global t_str
    A = t // 600
    B = ((t % 600) // 10) // 10
    C = ((t % 600) // 10) % 10
    D = (t % 600) % 10
    t_str = str(A) + ":" + str(B) + str(C) + "." + str(D)
    return t_str



# define helper function that counts number of total stops
#  and number of successful stops
def stop_count():
    global count_str
    count_str = str(x) + "/" + str(y)
    return count_str
    
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer_run
    timer.start()
    timer_run = True
    return timer_run



def stop():
    global x, y, count_str, timer_run
    if timer_run:        
        timer.stop()        
        y +=1
        if t_str[-1] == "0":
            x +=1
        stop_count()
        timer_run = False
    return count_str, timer_run



def reset():
    global t, x, y, count_str, timer_run
    timer.stop()
    t = 0
    format(t)
    x = 0
    y = 0
    stop_count()
    timer_run = False
    return t_str, count_str, timer_run    
                    
   
   
# define event handler for timer with 0.1 sec interval
def timer_tick():
    global t
    t +=1
    format(t)



# define draw handler
def draw(canvas):
    canvas.draw_text(t_str, [55, 85], 35, "White")
    canvas.draw_text(count_str, [155, 25], 28, "Green")
 
 
 
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 150)


# register event handlers
frame.add_button("Start", start, 120)
frame.add_button("Stop", stop, 120)
frame.add_button("Reset", reset, 120)
timer = simplegui.create_timer(100, timer_tick)
frame.set_draw_handler(draw)

# start frame
frame.start()
