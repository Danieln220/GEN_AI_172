#Goal: Create a dictionary that stores the indices (number of the position) of each letter in a word provided by the user(input()).
#1. User Input:
#Ask the user to enter a word.
#Store the input word in a variable.
#2. Creating the Dictionary:
#Iterate through each character of the input word using a loop.
#And check if the character is already a key in the dictionary.

word = input("type a word: ")

character_dict = {}

for index in range(len(word)):
    character = word[index]

    if character in character_dict:
        character_dict[character].append(index)
    else:
        character_dict[character] = [index]
print(character_dict)        


#Goal: Create a program that prints a list of items that can be purchased with a given amount of money.
#1. Store Data:
#You will be provided with a dictionary (items_purchase) where the keys are the item names and the values are their prices (as strings with a dollar sign). The priority is defined by the position of the iten on the dictionary: from the most important to the less important.
#You will also be given a string (wallet) representing the amount of money you have.
#2. Data Cleaning:
#You need to clean the dollar sign and the commas using python. Don’t hard code it.
#3. Determining Affordable Items:
#create a list called basket and add there the items that you can buy with the money you have on the wallet
#Don’t forget to update the wallet after buying an item.
#If the basket is empty (no items can be afforded), return the string “Nothing”.
#Otherwise, print the basket list in alphabetical order.

item_pusrchase = {}
wallet = ""

wallet = wallet.replace("$", "").replace(",", "")
wallet = int(wallet)

basket = []

for item, price in item_pusrchase.items():
    clean_price = price.replace("$", "").replace(",", "")
    clean_price = int(clean_price)

    if wallet >= clean_price:
        basket.append(item)
        wallet -= clean_price
if len(basket) == 0:
    print("nothing")
else:
    print(sorted(basket))

