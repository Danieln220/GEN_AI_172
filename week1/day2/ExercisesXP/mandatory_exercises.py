#exercise 1
#Print the following output using one line of code:

#Hello world
#Hello world
#Hello world
#Hello world

hello = "hello world"

print(hello * 4)

#exercise 2
#Write code that calculates the result of:

#(99^3)*8 (meaning 99 to the power of 3, times 8).

print(99 ** 3 * 8)

#exercise 3
#Predict the output of the following code snippets:
#Coment what is your guess, then run the code and compare
#Example:
#>>> 15 < 8 #False
expression1 = 5 < 3 #False
expession2 = 3 == 3 #True
experssion3 = 3 == "3" #False
expression4 = "3" > 3 #False
expression5 = "Hello" == "hello" #False

#exercise 4
#Create a variable called computer_brand which value is the brand name of your computer.
#Using the computer_brand variable, print a sentence that states the following:
#"I have a <computer_brand> computer."

computer_brand = "msi"

print(f"i have a {computer_brand} computer")

#exercise 5
#Create a variable called name, and set it’s value to your name.
#Create a variable called age, and set it’s value to your age.
#Create a variable called shoe_size, and set it’s value to your shoe size.
#Create a variable called info and set it’s value to an interesting sentence about yourself. The sentence must contain all the variables created in parts 1, 2, and 3.
#Have your code print the info message.
#Run your code.


name = "Daniel"
age = 24
shoe_size = 45
info = (f"Hello my name is {name} and im {age} years old and my shoe size is {shoe_size}!? ")
print(info)

#exercise 6
#Create two variables, a and b.
#Each variable’s value should be a number.
#If a is bigger than b, have your code print "Hello World".

a = 10
b = 5

if a > b:
    print("Hello world")


#exercise 7
#Write code that asks the user for a number and determines whether this number is odd or even.
num = int(input("choose a number: "))

if num % 2 == 0:
    print(f"the number {num} is even")
else:
    print(f"the number {num} is not even")


#exercise 8
#Write code that asks the user for their name and determines whether or not you have the same name. Print out a funny message based on the outcome.

name = input("write your name: ")

if name == "Daniel":
    print(f"welcome {name}, to the secret Daniel society")
else:
    print("you dont have a cool name")    


#exercise 9
#Write code that will ask the user for their height in centimeters.
#If they are over 145 cm, print a message that states they are tall enough to ride.
#If they are not tall enough, print a message that says they need to grow some more to ride.

user_height = int(input("write your hight in centimeters please: "))

if user_height > 145:
    print("you are tall enough to ride")
else:
    print("you need to grow more to ride")    
