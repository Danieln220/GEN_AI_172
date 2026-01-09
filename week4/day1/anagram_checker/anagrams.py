#Step3
# Now create another Python file, called anagrams.py. This will contain all the UI (user interface) functionality of your program, and will rely on AnagramChecker for the anagram-related logic.
# It should do the following
# Show a menu, offering the user to input a word or exit. Keep showing the menu until the user chooses to exit.
# If the user chooses to input a word, it must be accepted from the user’s keyboard input, and then be validated:
# Only a single word is allowed. If the user typed more than one word, show an error message. (Hint: how do we know how many words were typed?)
# Only alphabetic characters are allowed. No numbers or special characters.
# Whitespace should be removed from the start and end of the user’s input.
# Once your code has decided that the user’s input is valid, it should find out the following:
# All possible anagrams to the user’s word.
# Create an AnagramChecker instance and apply it to the steps created above.
# Display the information about the word in a user-friendly, nicely-formatted message such as:

from anagram_checker import AnagramChecker

def main():
    checker = AnagramChecker()

    while True:
        print("---- ANAGRAM CHECKER ----")
        user_input = input("Enter a word or type 'exit' to quit: ").strip()

        if user_input == 'exit':
            break

        if " " in user_input:
            print("Please enter only one word")
            continue

        if not user_input.isalpha():
            print("only characters not numbers")
            continue

        word = user_input.upper()
        if checker.is_valid_word(word):
            anagrams = checker.get_anagrams(word)

            print(f" YOUR WORD: {word}")
            print("This is a real English word")

            if anagrams:
                print(f"Anagrams for your word are: {', '.join(anagrams)}")
            else:
                print("no anagrams for this word")

        else:
            print(f"{word} is not a valid English word")

if __name__ == "__main__":
    main()