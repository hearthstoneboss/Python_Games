# implementation of card game - Memory
#http://www.codeskulptor.org/#save2_2hpNwAK3Ek.py
import simplegui
import random

#helper function to initialize globals
def new_game():
    global number,exposed,state,lindex,counter
    number = range(0,8)*2#random number
    random.shuffle(number)
    exposed = [False]*16#card exposed flag
    state = 0#State 0 corresponds to the start of the game
    #State 1 corresponds to a single exposed unpaired card
    #State 2 corresponds to the end of a turn
    lindex = []#two exposed card number
    counter = 0#number of turn
    l.set_text('Turns = '+str(counter))
    
#define event handlers
def mouseclick(pos):
    global exposed,state,lindex,counter
    index = pos[0]//50
    if state == 0:
        exposed[index] = True
        lindex.append(index)
        state = 1
    elif state == 1 and exposed[index] == False:
        exposed[index] = True
        lindex.append(index)
        state = 2
    elif state ==2 and exposed[index] == False:
        exposed[index] = True
        lindex.append(index)
        if number[lindex[0]] != number[lindex[1]]:
            exposed[lindex[0]] = False
            exposed[lindex[1]] = False
        lindex.pop(0)
        lindex.pop(0)
        state = 1
        counter += 1
        l.set_text('Turns = '+str(counter))

#cards are logically 50x100 piexls in size
def draw(canvas):
    global number,exposed
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(number[i]),(i*50,100),100,'White')
        else:
            canvas.draw_polygon([(50*i, 0), (50*i, 100), (50*(i+1), 100),(50*(i+1),0)], 1,'Yellow','Green')
    
#create frame and add a button and labels
frame = simplegui.create_frame('Memory',800,100)
frame.add_button('Restart',new_game)
l=frame.add_label('Turns = 0')

#register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

#get things rolling
new_game()
frame.start()
