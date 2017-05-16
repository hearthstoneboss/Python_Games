# http://www.codeskulptor.org/#user40_ete3vjlmonMsskL.py
# template for "Stopwatch: The Game"
import simplegui
# define global variables
time_ts = 0# time in tenths of seconds
x=0
y=0# x is the number of successful stops and y is number of total stops

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    a=t//600
    b=(t-a*600)//100
    c=(t//10)%10
    d=t%10
    return str(a)+":"+str(b)+str(c)+"."+str(d)
    
        
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
def stop():
    timer.stop()
def reset():
    global time_ts
    time_ts=0
    timer.stop()
    

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time_ts
    time_ts+=1

# define draw handler
def draw_handler(canvas):
    global time_ts
    if time_ts < 6000:
        str_write = format(time_ts)
        canvas.draw_text(str_write,(100,150),48,'Red')
    str2_write = str(x)+"/"+str(y)
    canvas.draw_text(str2_write,(250,0),48,'White')
    
# create frame
frame=simplegui.create_frame("Stopwatch",300,300)

# register event handlers
frame.add_button("Start",start,200)
frame.add_button("Stop",stop,200)
frame.add_button("Reset",reset,200)

frame.set_draw_handler(draw_handler)

timer=simplegui.create_timer(100,timer_handler)
# start frame
frame.start()

# Please remember to review the grading rubric


            
    
