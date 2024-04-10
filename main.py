#Simple number guessing game

numbertoguess = 5

while True:
    guess = int(input("Guess the number: "))
    if guess == numbertoguess:
        print("You guessed it!")
        break
    else:
        print("Try again!")
