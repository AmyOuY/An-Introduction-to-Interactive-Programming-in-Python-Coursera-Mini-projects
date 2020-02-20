# Implementation of card game - Memory


import simplegui
import random


#global variables
card = []
exposed = []
i = 0
j = 0
k = 0
state = 0
turns = 0



# helper function to initialize globals
def new_game():
    global card, exposed, state, turns    
    card = range(8)
    card.extend(range(8))
    random.shuffle(card)    
    exposed = [False for i in range(16)]
    state = 0
    turns = 0

    label.set_text("Turns = " + str(turns))
   
   
   
# define event handlers
def mouseclick(pos):
    global exposed, state, i, j, k, turns
    
    if exposed[pos[0] // 50] == True:
        return
    
    else:
        if state == 0:
            i = pos[0] // 50
            exposed[i] = True
            state = 1    
    
        elif state == 1:
            j = pos[0] // 50        
            exposed[j] = True
            turns +=1
            state = 2
                
        else:
            if card[i] != card[j]:
                exposed[i] = False            
                exposed[j] = False
        
            k = pos[0] // 50        
            exposed[k] = True            
            i = k                                
            state = 1

    label.set_text("Turns = " + str(turns))
                       
        
        
# cards are logically 50x100 pixels in size    
def draw(canvas):    
        
    for i in range(len(exposed)):            
        if exposed[i] == True:            
            canvas.draw_polygon([[i * 50, 0], [(i + 1) * 50, 0], [(i + 1) * 50, 100], [i * 50, 100]], 1, "Black", "Black")
            canvas.draw_text(str(card[i]), [i * 50 + 12, 70], 50, "White")            
        
        else:
            canvas.draw_polygon([[i * 50, 0], [(i + 1) * 50, 0], [(i + 1) * 50, 100], [i * 50, 100]], 1, "Red", "Green")
   
   
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


# get things rolling
new_game()
frame.start()
