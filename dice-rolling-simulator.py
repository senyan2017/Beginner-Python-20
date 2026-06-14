#importing module for random number generation
import random

#range of the values of a dice
min_val = 1
max_val = 6


#loop: keep rolling until user says no
while True:
    print("Rolling The Dices...")
    print("The Values are :")

    #generating and printing two random integers (a pair of dice)
    dice1 = random.randint(min_val, max_val)
    dice2 = random.randint(min_val, max_val)
    print(dice1)
    print(dice2)

    #ask user whether to roll again
    again = input("Roll the dice again? (y/n): ").strip().lower()
    if again != 'y':
        print("Thanks for playing!")
        break
