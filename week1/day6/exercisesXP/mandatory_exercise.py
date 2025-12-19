# Exercise 1: Converting Lists into Dictionaries
#Key Python Topics:
#Creating dictionaries
#Zip function or dictionary comprehension
#Instructions
#You are given two lists. Convert them into a dictionary where the first list contains the keys and the second list contains the corresponding values.

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

print(list(zip(keys, values)))


#exercise2
#Write a program that calculates the total cost of movie tickets for a family based on their ages.
#Family members’ ages are stored in a dictionary.
#The ticket pricing rules are as follows:
#Under 3 years old: Free
#3 to 12 years old: $10
#Over 12 years old: $15

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}
total_cost = 0

for name, age in family.items():
    if age < 3:
        price = 0
    elif 3 <= age <= 12:
        price = 10
    else:
        price = 15
    total_cost += price

    print(f"{name}: ${price}")

print(f"total cost: ${total_cost}")  


#exercise3
#Create and manipulate a dictionary that contains information about the Zara brand.
#Create a dictionary called brand with the provided data.
#Modify and access the dictionary as follows:
#Change the value of number_stores to 2.
#Print a sentence describing Zara’s clients using the type_of_clothes key.
#Add a new key country_creation with the value Spain.
#Check if international_competitors exists and, if so, add “Desigual” to the list.
#Delete the creation_date key.
#Print the last item in international_competitors.
#Print the major colors in the US.
#Print the number of keys in the dictionary.
#Print all keys of the dictionary.

brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": "blue",
        "Spain": "red",
        "US": ["pink", "green"]
    }
}

brand["number_stores"] = 2

clothes = brand["type_of_clothes"]
print(f"zara have a lot of diveres clients such as: {clothes}")
brand["country_creation"] = "spain"

if "international_competitors" in brand:
    brand["international_competitors"].append("desigual")

del brand["creation_date"]

competitor = brand["international_competitors"]
print("the last competitor is :", competitor[-1])

us_major_colors = brand['major_color']['US']
print(us_major_colors)

number_of_keys = len(brand)
print(f"there {number_of_keys} keys in the dict")

print(brand.keys())


#exercise4
#You are given a list of Disney characters. Create three dictionaries based on different patterns as shown below:
#Character List:
#users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]
#Create a dictionary that maps characters to their indices:
#Create a dictionary that maps indices to characters:
#Create a dictionary where characters are sorted alphabetically and mapped to their indices:

users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]
user_dict = {}

for index, name in enumerate(users):
    user_dict[name] = index

print(user_dict)  

index_dict = {i: users[i] for i in range(len(users))}

print(index_dict)

sorted_user_dict = {name: index for index, name in enumerate(sorted(users))}

print(sorted_user_dict)



