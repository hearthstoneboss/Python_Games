# Implementation of classic arcade game Pong
#http://www.codeskulptor.org/#user40_RWGPmBJqA7q4ffO.py
import simplegui
import random

#initialize globals - pos and vel encode vertical info for paddles
width = 600
height = 400
ball_radius = 20
pad_width = 8
pad_height = 80
half_pad_width = pad_width/2
half_pad_height = pad_height/2
left = False
right = True
#initialize globals - pos and vel encode vertical info for ball
ball_pos = [200,200]
ball_vel = [10,10]

#initialize ball_pos and ball_vel for new ball in middle of table
#if direction is right,the ball's velocity is upper right,else upper left
def spawn_ball(direction):
    global ball_pos,ball_vel#these are vectors stored as lists

    ball_pos[0] = width/2
    ball_pos[1] = height/2
    if direction:
        ball_vel[0] =random.randrange(120, 240)/60
        ball_vel[1] =-random.randrange(60, 180)/60
    else:
        ball_vel[0] =-random.randrange(120, 240)/60
        ball_vel[1] =-random.randrange(60, 180)/60

#define event handlers
def new_game():#restart button
    global paddle1_pos,paddle2_pos,paddle1_vel,paddle2_vel #these are numbers
    global score1,score2 #these are ints
    paddle1_pos = 100
    paddle2_pos = 100
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(right)


def draw(canvas):
    global score1,score2,paddle1_pos,paddle2_pos,ball_pos,ball_vel

    #draw mid line and qutters
    canvas.draw_line([width/2,0],[width/2,height],1,"White")
    canvas.draw_line([pad_width,0],[pad_width,height],1,"White")
    canvas.draw_line([width-pad_width,0],[width-pad_width,height],1,"White")

    #update ball
    if ball_pos[1] >= height-ball_radius or ball_pos[1] <= ball_radius:#ball collides with and bounces off of the top and bottom walls
        ball_vel[1] = -ball_vel[1]

    if ball_pos[0] <= ball_radius+pad_width:#ball collides with and bounces off of the left and right gutters or paddles
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos+pad_height:
            ball_vel[0] = -ball_vel[0]*1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            score2 += 1
            spawn_ball(right)
    elif ball_pos[0] >= width-ball_radius-pad_width:
        if ball_pos[1] > paddle2_pos and ball_pos[1] < paddle2_pos+pad_height:
            ball_vel[0] = -ball_vel[0]*1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            score1 += 1
            spawn_ball(left)
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    #draw ball
    canvas.draw_circle(ball_pos,ball_radius,1,"White","White")

    #update paddle's vertical position,keep paddle on the screen
    paddle1_pos += paddle1_vel
    if paddle1_pos < 0:
        paddle1_pos = 0
    elif paddle1_pos > height - pad_height:
        paddle1_pos = height - pad_height

    paddle2_pos += paddle2_vel
    if paddle2_pos < 0:
        paddle2_pos = 0
    elif paddle2_pos > height - pad_height:
        paddle2_pos = height - pad_height

    #draw paddles
    canvas.draw_polygon([(0,paddle1_pos),(pad_width,paddle1_pos),(pad_width,paddle1_pos+pad_height),(0,paddle1_pos+pad_height)],1,"White","White")
    canvas.draw_polygon([(width,paddle2_pos),(width-pad_width,paddle2_pos),(width-pad_width,paddle2_pos+pad_height),(width,paddle2_pos+pad_height)],1,"White","White")

    #draw scores
    canvas.draw_text(str(score1), (200, 50), 48, 'Red')
    canvas.draw_text(str(score2), (400, 50), 48, 'Red')

def keydown(key):
    global paddle1_vel,paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5

def keyup(key):
    global paddle1_vel,paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

#create frame
frame = simplegui.create_frame("Pong",width,height)

# register event handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",new_game,200)

#start frame
new_game()
frame.start()
