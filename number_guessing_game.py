import random

def number_guessing_game():
    random_number = random.randint(1, 100)
    max_attempts = 7
    
    print("welcome to the number guessing game!")
    print("select the number between 1 - 100")
    print("you have 7 attempts")
    print("Good luck!")

    for attempt in range(1, max_attempts + 1):
        guess = int(input(f"attempt {attempt} / {max_attempts} "))

        if guess < random_number:
            print("Too low")
        elif guess > random_number:
            print("Too high")
        else:
            print(f"Congratulations! you guessed the number {random_number}")
            return
    print(f"Your correct answer was {random_number}")     

number_guessing_game()         
          
                    

    

   



