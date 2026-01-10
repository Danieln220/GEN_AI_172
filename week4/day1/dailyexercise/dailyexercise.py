# Part 1 : Quizz :
# Answer the following questions
# What is a class?
# answer: A blueprint or template used to create objects that define common properties and behaviors.
# What is an instance?
#answer: A specific object created from a class (e.g., if "Dog" is the class, "Snoopy" is the instance).
# What is encapsulation?
#answer: Hiding the internal data of an object and only allowing access through specific methods to keep it safe.
# What is abstraction?
#answer: Hiding complex background details and only showing the essential features to the user.
# What is inheritance?
#answer: A way for one class (child) to take on the attributes and methods of another class (parent).
# What is multiple inheritance?
#answer: A feature where a class can inherit behaviors from more than one parent class at the same time.
# What is polymorphism?
#answer: The ability for different classes to be treated as the same type, often by having methods with the same name that act differently.
# What is method resolution order or MRO?
#answer: The specific order in which Python looks for a method in a hierarchy of classes.




# Part 2: Create a deck of cards class.
# The Deck of cards class should NOT inherit from a Card class.
# The requirements are as follows:
# The Card class should have a suit (Hearts, Diamonds, Clubs, Spades) and a value (A,2,3,4,5,6,7,8,9,10,J,Q,K)
# The Deck class :
# should have a shuffle method which makes sure the deck of cards has all 52 cards and then rearranges them randomly.
# should have a method called deal which deals a single card from the deck. After a card is dealt, it should be removed from the deck.

from random import shuffle

suits = ["Hearts", "Diamonds","Clubs", "Spades"]
value = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in suits for v in  value]

    def shuffle(self):
        if len(self.cards) == 52:
            shuffle(self.cards)
            print('deck shuffled')
        else:
            print("cannot shuffle the deck is incomplete")

    def deal(self):
        if not self.cards:
            return "the deck is empty"
        
        dealt_card = self.cards.pop()
        return dealt_card
    
my_deck = Deck()
my_deck.shuffle()
card = my_deck.deal()
print(f"you delt the {card}")
