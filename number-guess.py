from random import randint

rand_num = randint(0, 100)  # random number in range 0 to 100
guessCheck = "wrong"  # for controlling the loop

print("Welcome to Number Guess")

#loop
while guessCheck == "wrong":
    try:
        raw = input("Please input a number between 0 and 100: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break

    # validate input: must be an integer
    try:
        user_input = int(raw)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        continue

    # validate range
    if user_input < 0 or user_input > 100:
        print("Out of range. Please enter a number between 0 and 100.")
        continue

    #checks for the correctness of guess
    if user_input < rand_num:
        print("Its Lower than actual number. Try Again.")  # if guess is lower, loop continues
    elif user_input > rand_num:
        print("Its Higher than actual number. Try Again.")  # if guess is higher, loop continues
    else:
        print("Bravo, You Got It!")
        guessCheck = "correct"  # if guess is correct, terminate loop

print("Thank You for Playing Number Guess. See You Again")
