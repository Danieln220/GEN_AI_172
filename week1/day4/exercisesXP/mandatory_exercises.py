#exercise1
#Create a set called my_fav_numbers and populate it with your favorite numbers.
#Add two new numbers to the set.
#Remove the last number you added to the set.
#Create another set called friend_fav_numbers and populate it with your friend’s favorite numbers.
#Concatenate my_fav_numbers and friend_fav_numbers to create a new set called our_fav_numbers.
#Note: Sets are unordered collections, so ensure no duplicate numbers are added.

my_fav_numbers = {5, 8, 22, 24, 78, 65, 10}

my_fav_numbers.add(13)
my_fav_numbers.add(32)

my_fav_numbers.remove(65)

friends_fav_numbers = {50, 60, 70, 80}

our_fav_numbers = my_fav_numbers.union(friends_fav_numbers)

print(our_fav_numbers)

#exercise2
#Given a tuple of integers, try to add more integers to the tuple.
#Hint: Tuples are immutable, meaning they cannot be changed after creation. Think about why you can’t add more integers to a tuple.

my_tuple = (1, 2, 3, 4)

new_tuple = my_tuple + (5, 6)

print(my_tuple)
print(new_tuple)
#because tuples are immutable i just created a new tuple and merged the first tuple set with 2 additional numbers that i chose.

#exercise3
#You have a list: basket = ["Banana", "Apples", "Oranges", "Blueberries"]
#Remove "Banana" from the list.
#Remove "Blueberries" from the list.
#Add "Kiwi" to the end of the list.
#Add "Apples" to the beginning of the list.
#Count how many times "Apples" appear in the list.
#Empty the list.
#Print the final state of the list.

basket = ["banana", "apples", "oranges", "blueberries"]

basket.remove("banana")
basket.remove("blueberries")
basket.append("kiwi")
basket.insert(0, "apples")
basket.count("apples")
basket.clear()

print(basket)

#exercise4
#Recap: What is a float? What’s the difference between a float and an integer?
#Create a list containing the following sequence of mixed types: floats and integers:
#1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.
#Avoid hard-coding each number manually.
#Think: Can you generate this sequence using a loop or another method?

numers_list = []
x = 1.5
while x <= 5:
    numers_list.append(x)
    x += 0.5
print(numers_list)    


#exercise5
#Write a for loop to print all numbers from 1 to 20, inclusive.
#Write another for loop that prints every number from 1 to 20 where the index is even.

for num in range(1, 21):
    print(num)

for n in range(2, 21, 2):
    print(n)  

#exercise6
#Use an input to ask the user to enter their name.
#Using a while True loop, check if the user gave a proper name (not digits and at least 3 letters long)
#hint: check for the method isdigit()
#if the input is incorrect, keep asking for the correct input until it is correct
#if the input is correct print “thank you” and break the loop
while True:
    user_name = input("enter your name please: ")

    if len(user_name) < 3:
        print("name too short")
    else:
        has_number = False

        for character in user_name:
            if character.isdigit():
                has_number = True
        if has_number == True:
            print("you cant have number in your name")
        else:
            print("thank you")
            break    
         
   
#exercise7
#Ask the user to input their favorite fruits (they can input several fruits, separated by spaces).
#Store these fruits in a list.
#Ask the user to input the name of any fruit.
#If the fruit is in their list of favorite fruits, print:
#"You chose one of your favorite fruits! Enjoy!"
#If not, print:
#"You chose a new fruit. I hope you enjoy it!"

user_fruits = input("type your fav fruits using spaces: ")

fav_fruits = user_fruits.split()

fruit_chosen = input("enter a name of a fruit: ")

if fruit_chosen in fav_fruits:
    print("you chose one of your favorite fruits!")
else:
    print("you chose a new fruit. i hope you enjoy it!")


#exercise8
#Write a loop that asks the user to enter pizza toppings one by one.
#Stop the loop when the user types 'quit'.
#For each topping entered, print:
#"Adding [topping] to your pizza."
#After exiting the loop, print all the toppings and the total cost of the pizza.
#The base price is $10, and each topping adds $2.50.

toppings = []
pizza_price = 10.00
topping_price = 2.50

print("pizza shop")
print("when you finish ordering type 'quit'")

while True:
    topping_choice = input("what topping you want? ")

    if topping_choice == "quit":
        break
    toppings.append(topping_choice)
    print(f"adding {topping_choice} to your pizza")

number_of_toppings = len(toppings)
total_price = pizza_price + number_of_toppings * topping_price

print(f"your toppings are: {toppings}")
print(f"total number of toppings: {number_of_toppings}")
print(f"the total price is: ${total_price}")


#exercise9
#Ask for the age of each person in a family who wants to buy a movie ticket.
#Calculate the total cost based on the following rules:
#Free for people under 3.
#$10 for people aged 3 to 12.
#$15 for anyone over 12.
#Print the total ticket cost.

total_cost = 0
family_size = 0

print("cinema counter")
print("type 'finish' when you entered everybody")

while True:
    user_input = input("enter your ages: ")

    if user_input == "finish":
        break

    age = int(user_input)
    family_size = family_size + 1

    if age < 3:
        ticket_price = 0
        print(f"your age {age}: the ticket is free")
    elif age <= 12:
        ticket_price = 10
        print(f"your age is {age}: the ticket is 10$")
    else:
        ticket_price = 15
        print(f"your age is {age}: the ticket is 15$")

    total_cost = total_cost + ticket_price
print(f"the total ticket cost for your family is: ${total_cost}")
                        









