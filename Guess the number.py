# "Guess the number" mini-project

# input will come from buttons and an input field
# all output for the game will be printed in the console


import simplegui
import random
import math


# initialize global variables 
secret_num = 0
num_range = 100
count = 0



# helper function to start and restart the game
def new_game():
    global secret_num, num_range, count
    secret_num = random.randrange(0, num_range)
    count = int(math.ceil(math.log(num_range + 1, 2)))    
    print "New game. Range is from 0 to", num_range    
    print "Number of remaining guesses is", count
    return secret_num, count                                
            


# define event handlers for control panel
def range100():      
    print
    global num_range
    num_range = 100
    new_game()
      
 
 
def range1000():
    print
    global num_range
    num_range = 1000    
    new_game()

    
    
def input_guess(guess):
    print
    global secret_num, count
    count -=1
    guess = int(guess)
    print "Guess was", guess
    print "Number of remaining guesses is", count
    if count > 0:
        if guess > secret_num:        
            print "Lower!"
        elif guess < secret_num:
            print "Higher!"
        elif guess == secret_num:
            print "Correct!"
            print
            new_game()
    elif count == 0 and guess == secret_num:
        print "Correct!"
        print
        new_game()
    else:
        print "You ran out of guesses. The number was", secret_num
        print
        new_game()

   
  
  
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)


# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame
new_game()
f.start()
