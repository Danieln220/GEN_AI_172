#Using map and filter, try to say hello to everyone who's name is less than or equal to 4 letters
people = ["Rick", "Morty", "Beth", "Jerry", "Snowball"]

filtered_list = filter(lambda name: len(name)<= 4, people)
mapped_list = map(lambda name: f"hello {name}", filtered_list)

