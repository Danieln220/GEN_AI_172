# Create a new file called anagram_checker.py which contains a class called AnagramChecker.
# The class should have the following methods:
# __init__ - should load the word list file (text file) into a variable, so that it can be searched later on in the code.
# is_valid_word(word) – should check if the given word (ie. the word of the user) is a valid word.
# get_anagrams(word) – should find all anagrams for the given word. (eg. if word of the user is ‘meat’, the function should return a list containing [“mate”, “tame”, “team”].)
# Hint: you might want to create a separate method called is_anagram(word1, word2), that will compare 2 words and return True if they contain the same letters (but not in the same order), and False if not.
# Note: None of the methods in the class should print anything.

class AnagramChecker:
    def __init__(self, file_path="sowpods.txt"):
        with open(file_path, 'r') as f:
            self.word_list = [line.strip().upper() for line in f]
         
    def is_valid_word(self, word: str):
        return word.upper() in self.word_list
    
    def is_anagram(self, word1, word2):
        word1 = word1.upper()
        word2 = word2.upper()
        return sorted(word1) == sorted(word2) and word1 != word2
    
    def get_anagrams(self, word1):
        word1 = word1.upper()
        anagrams = [w for w in self.word_list if self.is_anagram(word1, w)]
        return anagrams