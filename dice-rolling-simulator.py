#importing module for random number generation
import random

#range of the values of a dice
min_val = 1
max_val = 6
dice


#loop
while max_val != 2:
    print("Rolling The Dices...")
    print("The Values are :")
    
    #generating and printing 1st random integer from 1 to 6
    dice = random.randint(min_val, max_val)
    print(dice)
    
