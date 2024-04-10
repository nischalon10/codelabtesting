#Simple number guessing game
import random

numbertoguess = random.randint(1, 100)

while True:
    guess = int(input("Guess the number: "))
    if guess == numbertoguess:
        print("You guessed it!")
        break
    else:
        print("Try again!")
