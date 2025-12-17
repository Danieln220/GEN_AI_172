#exercise1
#Ask the user for two inputs:
#A number (integer).
#A length (integer).
#2. Create a program that generates a list of multiples of the given number.
#3. The list should stop when it reaches the length specified by the user.

num = int(input("enter your number: "))
length = int(input("enter your multiplies number: "))

multiplies_list = []

for i in range(1, length + 1):
    result = num * i
    multiplies_list.append(result)

print(f"this is the multiples list: {multiplies_list}")    


#exercise2
#Ask the user for a string.
#2. Write a program that processes the string to remove consecutive duplicate letters.
#The new string should only contain unique consecutive letters.
#For example, “ppoeemm” should become “poem” (removes consecutive duplicates like ‘pp’, ‘ee’, and ‘mm’).
#3. The program should print the modified string.

user_string = input("enter a word: ")

new_string = ""

last_letter_seen = ""

for letter in user_string:
    
    if letter != last_letter_seen:
        
        new_string = new_string + letter
        
        last_letter_seen = letter

print(f"modified string: {new_string}")  
