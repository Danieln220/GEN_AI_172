<<<<<<< HEAD

numbers = [1, 2, 3, 4]
for n in numbers:
    print(n)

for n in numbers:
    print(n * 20)

names = ["Elie", "Tim", "Matt"]
for name in names:
    first_letter = name[0]
    print(first_letter)

numbers_2 = [1, 2, 3, 4, 5, 6]
even_numbers = []  
for num in numbers:
    
    if num % 2 == 0:
        even_numbers.append(num)

print(even_numbers)

list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]

set1 = set(list1)
set2 = set(list2)

same_numbers_set = set1 & set2
same_numbers_list = list(same_numbers_set)
print(same_numbers_list)

words = ["Elie", "Tim", "Matt"]
reversed_words_lowercase = [word[::-1].lower() for word in words]

print(reversed_words_lowercase)

string1 = "first"
string2 = "third"

set11 = set(string1)
set22 = set(string2)
letters_set = set11 & set22
letters_list = list(letters_set)
print(letters_list)   

numbers = range(1, 101)
divided_by_12 = [num for num in numbers if num % 12 == 0]
print(divided_by_12)

word_string = "amazing"
vowels = "aeiou"


amazing_vowels = [char for char in word_string if char not in vowels]
print(amazing_vowels)

ten_list = [0, 1, 2] * 3
print(ten_list)

eleven_list = list(range(10))
eleven_list_short = [eleven_list] * 10
print(eleven_list_short)

=======

numbers = [1, 2, 3, 4]
for n in numbers:
    print(n)

for n in numbers:
    print(n * 20)

names = ["Elie", "Tim", "Matt"]
for name in names:
    first_letter = name[0]
    print(first_letter)

numbers_2 = [1, 2, 3, 4, 5, 6]
even_numbers = []  
for num in numbers:
    
    if num % 2 == 0:
        even_numbers.append(num)

print(even_numbers)

list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]

set1 = set(list1)
set2 = set(list2)

same_numbers_set = set1 & set2
same_numbers_list = list(same_numbers_set)
print(same_numbers_list)

words = ["Elie", "Tim", "Matt"]
reversed_words_lowercase = [word[::-1].lower() for word in words]

print(reversed_words_lowercase)

string1 = "first"
string2 = "third"

set11 = set(string1)
set22 = set(string2)
letters_set = set11 & set22
letters_list = list(letters_set)
print(letters_list)   

numbers = range(1, 101)
divided_by_12 = [num for num in numbers if num % 12 == 0]
print(divided_by_12)

word_string = "amazing"
vowels = "aeiou"


amazing_vowels = [char for char in word_string if char not in vowels]
print(amazing_vowels)

ten_list = [0, 1, 2] * 3
print(ten_list)

eleven_list = list(range(10))
eleven_list_short = [eleven_list] * 10
print(eleven_list_short)

>>>>>>> 97acb61f3e8ba28a58ab0c8e991f93287df9522a
