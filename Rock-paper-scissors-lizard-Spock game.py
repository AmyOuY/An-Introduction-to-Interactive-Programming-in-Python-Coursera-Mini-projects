# Rock-paper-scissors-lizard-Spock game


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors



# convert name to a number using if/elif/else
def name_to_number(name):
    """converts the string name into a number between 0 and 4""" 
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    else:
        print "Error! Name does not match correct input"
    return number    



# convert number to a name using if/elif/else
def number_to_name(number):
    """converts a number in the range 0 to 4 into 
    its corresponding name as a string"""
    if number ==0:
        name = "rock" 
    elif number == 1:
        name = "Spock"   
    elif number ==2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        print "Error! Number is not in the correct range"
    return name    
    
    
     
# define rpsls function for determining winner     
import random
def rpsls(player_choice):
    """convert the player's choice to player_number,
    compute random guess for comp_number, and compute 
    their difference taken modulo five to determine winner""" 
    print
    print "Player chooses", str(player_choice)
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses", str(comp_choice)
    difference = comp_number - player_number 
    if difference % 5 == 1 or difference % 5 == 2:
        print "Computer wins!"
    elif difference % 5 == 3 or difference % 5 == 4:
        print "Player wins!"
    else:
        print "Player and computer tie!"
       

    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
