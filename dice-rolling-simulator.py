#importing module for random number generation
import random

#range of the values of a dice
min_val = 1
max_val = 6

#loop
while True:
    print("Rolling The Dices...")
    print("The Values are :")

    #generating and printing random integer from 1 to 6
    dice = random.randint(min_val, max_val)
    print(dice)

    roll_again = input("Roll again? (y/n): ").strip().lower()
    if roll_again != 'y':
        print("Thanks for playing!")
        break
