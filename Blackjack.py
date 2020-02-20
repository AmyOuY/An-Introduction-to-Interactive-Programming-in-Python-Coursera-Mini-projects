# Mini-project- Blackjack


import simplegui
import random


# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    


# initialize some useful global variables
outcome1 = ""
outcome2 = ""
score = 0
in_play = False
stand = True


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}



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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
   



# define hand class
class Hand:
    def __init__(self):
        self.card = []
        
    def __str__(self):
        ans = ""
        for i in range(len(self.card)):
            ans += str(self.card[i]) + " "
        return "Hand contains " + ans

    def add_card(self, card):
        self.card.append(card)          

    def get_value(self):
        self.value = 0
        for card in self.card:
            self.value += VALUES[card.get_rank()]
        if 'A' not in [card.get_rank() for card in self.card]:
            return self.value
        else:            
            if self.value + 10 <= 21:
                return self.value + 10
            else:
                return self.value
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.card:                                                 
            card.draw(canvas, [(CARD_SIZE[0] + 15) * i + 80, pos[1]])
            i += 1  
 
 
 
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:                
                self.deck.append(Card(suit, rank))        

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i]) + " "
        return "Deck contains " + ans



#define event handlers for buttons
def deal():
    global my_deck, dealer_hand, player_hand, outcome1, outcome2, score, in_play, stand
    my_deck = Deck()
    my_deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()    
    player_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())         
    player_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    outcome1 = ""
    stand = True    
    if in_play:
        outcome1 = "You lost!" 
        outcome2 = "New deal?"
        score -= 1
        in_play = False
        stand = False
    else:    
        outcome2 = "Hit or stand?"
        in_play = True

       
       
def hit():
    global outcome1, outcome2, score, in_play, stand
    if in_play:
        player_hand.add_card(my_deck.deal_card())
        if player_hand.get_value() > 21:        
            outcome1 = "You busted and lost!"
            outcome2 = "New deal?"
            score -= 1
            in_play = False
            stand = False
        else:
            outcome2 = "Hit or stand?"
            in_play = True

      
      
def stand():
    global outcome1, outcome2, score, in_play, stand    
    if stand:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
        
        if dealer_hand.get_value() > 21: 
            outcome1 = "Dealer busted and lost!"
            outcome2 = "New deal?"
            score += 1        
        else:     
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome1 = "You lost!"
                outcome2 = "New deal?"
                score -= 1
            else:        
                outcome1 = "You won!"
                outcome2 = "New deal?"
                score += 1
        stand = False        
    in_play = False
        
  
  
# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", [100, 70], 45, "Blue")
    canvas.draw_text("Dealer", [80, 170], 35, "Black")
    canvas.draw_text("Player", [80, 370], 35, "Black")
    canvas.draw_text(outcome1, [260, 160], 35, "White")
    canvas.draw_text(outcome2, [240, 350], 35, "White")
    canvas.draw_text("Score " + str(score), [420, 80], 35, "White")
    dealer_hand.draw(canvas, [70, 190])
    player_hand.draw(canvas, [70, 390])    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [80 + CARD_BACK_CENTER[0], 190 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
   


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
