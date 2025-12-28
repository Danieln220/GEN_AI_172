#Instructions
#The computer choose a random word and mark stars for each letter of each word.
#Then the player will guess a letter.
#If that letter is in the word(s) then the computer fills the letter in all the correct positions of the word.
#If the letter isn’t in the word(s) then add a body part to the gallows (head, body, left arm, right arm, left leg, right leg).
#The player will continue guessing letters until they can either solve the word(s) (or phrase) or all six body parts are on the gallows.
#The player can’t guess the same letter twice.

import random

wordslist = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share', 'credit card', 'rush', 'south']

def hidden_word(word):
    hidden = ""
    for letter in word:
        if letter == " ":
            hidden += " "
        else:
            hidden += "*"
    return hidden

def updated_hidden_word(word, hidden_word, guess):
    new_hidden_word = ""
    for i in range(len(word)):
        if word[i] == guess:
            new_hidden_word += guess
        else:
            new_hidden_word += hidden_word[i]
    return new_hidden_word

def game():
    word = random.choice(wordslist)
    hide_word = hidden_word(word)
    guessed_letters = []
    wrong_guesses = 0
    max_guesses = 6

    while wrong_guesses < max_guesses and "*" in hide_word:
        print(f"The word is: {hide_word}")
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print(f"You already guessed {guess}!")
            continue

        guessed_letters.append(guess)

        if guess in word:
            hide_word = updated_hidden_word(word, hide_word, guess)
            print(f"Yes! {guess} is in the word.")
        else:
            wrong_guesses += 1
            print(f"Wrong guess! Body parts: {wrong_guesses}/{max_guesses}")

    
    if "*" not in hide_word:
        print(f"You won! The word was: {word}")
    else:
        print(f"You lost! The word was: {word}")

game()