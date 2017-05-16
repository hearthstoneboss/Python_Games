#http://www.codeskulptor.org/#user40_RbtYFCrt6PuJ33I.py
# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
import simplegui
import math

guess_number=0
secret_number=0
n=0
flag=True

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number,n
    if flag == True:
        print "New game.Range is from 0 to 100"
        secret_number=random.randrange(0,100)
        n=int(math.ceil(math.log(100,2)))
    else:
        print "New game.Range is from 0 to 1000"
        secret_number=random.randrange(0,1000)
        n=int(math.ceil(math.log(1000,2)))
        
 
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global flag,n
    flag=True
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global flag,n
    flag=False
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global guess_number,n
    
    guess_number=int(guess)
    n=n-1
    
    print "Guess was "+guess
    print "Number of remaining guesses is",n
    if guess_number > secret_number:
        print "Higher"
    elif guess_number < secret_number:
        print "Lower"
    else:
        print "Correct"
        new_game()
        
    if n==0:
        new_game()
        
            
    
   

    
# create frame
frame=simplegui.create_frame("Guess the number",200,200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0,100)",range100,200)
frame.add_button("Range is [0,1000)",range1000,200)
frame.add_input("Enter a guess",input_guess,200)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric

