#Using map and filter, try to say hello to everyone who's name is less than or equal to 4 letters
people = ["Rick", "Morty", "Beth", "Jerry", "Snowball"]

filtered_pepople = filter(lambda s: len(people) >= 4, people)

print(filtered_pepople)