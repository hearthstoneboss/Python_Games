#Mini-project6 - Blackjack
#http://www.codeskulptor.org/#save2_dHg6otjvG1.py
import simplegui
import random

#load card sprite - 936x500 - 
#source: http://static.wixstatic.com/media/c286be_ff58dd53fa564c24b94549713250b2d1.gif thank Eugene Noore for providing this picture
CARD_SIZE = (72,100)
CARD_CENTER = (36,50)
card_images = simplegui.load_image("http://static.wixstatic.com/media/c286be_ff58dd53fa564c24b94549713250b2d1.gif")
#http://commondatastorage.googleapis.com/codeskulptor-assets/card.jfitz.png

#initialize some useful global variables
in_play = False
outcome = ""
score = 0

#define global for cards
SUITS = ('H','D','C','S')#H-Heart D-Diamond C-Club S-Spade
RANKS = ('A','2','3','4','5','6','7','8','9','T','J','Q','K')
VALUES = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':10,'Q':10,'K':10}

#define card class
class Card:
    def __init__(self,suit,rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ",suit,rank

    def __str__(self):
        return self.suit + self.rank
    
    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self,canvas,pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0]*RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1]*SUITS.index(self.suit))
        canvas.draw_image(card_images,card_loc,CARD_SIZE,[pos[0] + CARD_CENTER[0],pos[1] + CARD_CENTER[1]],CARD_SIZE)

#define hand class
class Hand:
    def __init__(self):
        self.hand_card = []

    def __str__(self):
        s = 'Hand cards consist of '
        for card in self.hand_card:
            s += (str(card)+' ')
        return s

    def add_card(self,card):
        self.hand_card.append(card)

    #count aces as 1,if the hand has an ace,then add 10 to hand values if it doesn't bust
    def get_value(self):
        value = 0
        card_rank = []
        for card in self.hand_card:
            rank = card.get_rank()
            card_rank.append(rank)
            value += VALUES[rank]

        if 'A' in card_rank:
            value += 10
            if value > 21:
                value -= 10

        return value

    def busted(self):
        pass

    def draw(self,canvas,p):
        i = 0
        pos = [0,0]
        for card in self.hand_card:
            pos[0] = (CARD_SIZE[0]+10)*i + p[0]
            pos[1] = p[1]
            i += 1
            card.draw(canvas,pos)

#define deck class
class Deck:
    def __init__(self):
        self.deck_card=[]
        for i in SUITS:
            for j in RANKS:
                card = Card(i,j)
                self.deck_card.append(card)

    #add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.deck_card)

    def deal_card(self):
        return self.deck_card.pop(0)

#define event handlers for buttons
def deal():
    global outcome,score,in_play,deck,dealer_hand,player_hand
    if not in_play:
        deck = Deck()
        deck.shuffle()
        #create new player and dealer hands
        dealer_hand = Hand()
        player_hand = Hand()
        #add two cards to each hand
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        outcome = ""
        in_play = True
    else:
        outcome = "You lose."
        score -= 1
        in_play = False

def hit():
    global in_play,outcome,score,deck,player_hand
    #if the hand is in play,hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    #if busted,assign an message to outcome,update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You lose."
            score -= 1
            in_play = False

def stand():
    global in_play,outcome,score,deck,dealer_hand,player_hand
    #if hand is in play,repeated hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
    #assign a message to outcome,update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = "You win."
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "You lose."
            score -= 1
        else:
            outcome = "You win."
            score += 1
    in_play = False

#draw handler
def draw(canvas):
    global in_play,outcome,score,player_hand,dealer_hand
    #draw dealer player hand
    dealer_hand.draw(canvas,[80,220])
    player_hand.draw(canvas,[80,420])
    #draw an image of the back of a card
    if in_play:
        canvas.draw_image(card_images,[900,450],CARD_SIZE,[116,270],CARD_SIZE)
    #draw text
    canvas.draw_text("Blackjack",(50,80),48,'White')
    canvas.draw_text("Score:"+str(score),(380,80),32,'White')
    canvas.draw_text("Dealer",(80,180),32,'White')
    canvas.draw_text(outcome,(280,180),32,'White')
    canvas.draw_text("Player",(80,380),32,'White')
    if in_play:
        canvas.draw_text("Hit or Stand?",(280,380),32,'White')
    else:
        canvas.draw_text("New deal?",(280,380),32,'White')

#initialization frame
frame = simplegui.create_frame("Blackjack",600,600)
frame.set_canvas_background('Green')

#create button and canvas callback
frame.add_button("Deal",deal,200)
frame.add_button("Hit",hit,200)
frame.add_button("Stand",stand,200)
frame.set_draw_handler(draw)

#deal an initial hand
deal()
#get things rolling
frame.start()
        
        
