#exercise1
# Instructions:
# Use the provided Pets and Cat classes to create a Siamese breed, instantiate cat objects, and use the Pets class to manage them.
# See the example below, before diving in.
# Step 1: Create the Siamese Class
# Create a class called Siamese that inherits from the Cat class.
# You can add any specific attributes or methods for the Siamese breed, or leave it as is if there are no unique behaviors.
# Step 2: Create a List of Cat Instances
# Create a list called all_cats that contains instances of Bengal, Chartreux, and Siamese cats.
# Example: all_cats = [bengal_obj, chartreux_obj, siamese_obj]
# Give each cat a name and age.
# Step 3: Create a Pets Instance
# Create an instance of the Pets class called sara_pets, passing the all_cats list as an argument.
# Step 4: Take Cats for a Walk
# Call the walk() method on the sara_pets instance.
# This should print the result of calling the walk() method on each cat in the list.


class Pets:
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat:
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'
    
class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    
class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    
class Siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    
cats_list = [Bengal('jhon', 5),
             Chartreux('sara', 2),
             Siamese('mark', 1)]

sara_pets = Pets(cats_list)
sara_pets.walk()


#exercise2
# Instructions:
# Step 1: Create the Dog Class
# Create a class called Dog with name, age, and weight attributes.
# Implement a bark() method that returns “<dog_name> is barking”.
# Implement a run_speed() method that returns weight / age * 10.
# Implement a fight(other_dog) method that returns a string indicating which dog won the fight, based on run_speed * weight.
# Step 2: Create Dog Instances
# Create three instances of the Dog class with different names, ages, and weights.
# Step 3: Test Dog Methods
# Call the bark(), run_speed(), and fight() methods on the dog instances to test their functionality.


class Dog:
    def __init__(self, name, age, weight):
       self.name = name
       self.age = age
       self.weight = weight

    def bark(self):
        return f'{self.name} is barking'

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        self_speed = self.run_speed() * self.weight
        other_dog_speed = other_dog.run_speed() * self.weight

        if self_speed > other_dog_speed:
            return f'{self.name} won the fight'
        elif other_dog_speed > self_speed:
            return f'{other_dog.name} won the fight'
        else:
            return 'its a draw'

# Step 2: Create dog instances
dog1 = Dog('tony', 2, 25)
dog2 = Dog('johnny', 5, 15)
dog3 = Dog('max', 4 , 10)

# Step 3: Test dog methods
print(dog1.bark())
print(dog2.run_speed())
print(dog1.fight(dog2))


#exercise4
# Instructions:
# Step 1: Create the Person Class
# Define a Person class with the following attributes:
# first_name
# age
# last_name (string, should be initialized as an empty string)
# Add a method called is_18():
# It should return True if the person is 18 or older, otherwise False.
# Step 2: Create the Family Class
# Define a Family class with:
# A last_name attribute
# A members list that will store Person objects (should be initialized as an empty list)
# Add a method called born(first_name, age):
# It should create a new Person object with the given first name and age.
# It should assign the family’s last name to the person.
# It should add this new person to the members list.
# Add a method called check_majority(first_name):
# It should search the members list for a person with that first_name.
# If the person exists, call their is_18() method.
# If the person is over 18, print:
# "You are over 18, your parents Jane and John accept that you will go out with your friends"
# Otherwise, print:
# "Sorry, you are not allowed to go out with your friends."
# Add a method called family_presentation():
# It should print the family’s last name.
# Then, it should print each family member’s first name and age.

class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age
        self.last_name = " "

    def is_18(self):
        return self.age >= 18
    
class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def born(self, first_name, age):
        new_person = Person(first_name, age)
        new_person.last_name = self.last_name
        self.members.append(new_person)

    def check_majority(self, first_name):
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print('You are over 18, your parents Jane and John accept that you will go out with your friends')
                else:
                    return print(f'Sorry {first_name}, you are not allowed to go out with your friends.') 

    def family_presentation(self):
        print(f'the {self.last_name} family!')
        for member in self.members:
            print(f'first name: {member.first_name}, age: {member.age}')

jarvis_family = Family('Jarvis')
jarvis_family.born('tommy', 19)
jarvis_family.born('max', 10)
jarvis_family.check_majority('tommy')
jarvis_family.check_majority('max')
jarvis_family.family_presentation()


