# TODO
from random import randint
number = randint(1,101)
cnt = 0
while True:
    guess = int(input("Please guess the number from 1-100: "))
    cnt += 1
    if (guess == number):
        print(f"You guess it right with {cnt} time")
        break
    elif(guess < number):
        print("Your guess is low")
    else:
        print("Your guess is High")
