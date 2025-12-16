
list = [("name", "elie"), ("job", "instructor")]
dictionary = dict(list)
print(list)

list1 = ["CA", "NJ", "RI"]
list2 = ["California", "New Jersey", "Rhode Island"]
dictionary2 = dict(zip(list1, list2))
print(dictionary2)

vowels = ['a', 'e', 'i', 'o', 'u']
vowels_dictionary = {}
for vowel in vowels:
    vowels_dictionary[vowel] = 0

print(vowels_dictionary)

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet_map = {}
position = 1
for letter in alphabet:
    alphabet_map[position] = letter
    position = position + 1
print(alphabet_map)    

