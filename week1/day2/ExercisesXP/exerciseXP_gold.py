#exercise1
#Print the following output in one line of code:
#Hello world
#Hello world
#Hello world
#Hello world
#I love python
#I love python
#I love python
#I love python

print("hello world" * 4, "i love python" * 4)



#exercise2
#Ask the user to input a month (1 to 12).
#Display the season of the month received :
#Spring runs from March (3) to May (5)
#Summer runs from June (6) to August (8)
#Autumn runs from September (9) to November (11)
#Winter runs from December (12) to February (2)

user_month = int(input("choose a month form 1 - 12: "))

if 3 >= user_month <= 5:
    print("the season is spring")
elif 6 >= user_month <= 8:
    print("the season is summer")
elif 9 >= user_month <= 11:
    print("the season is autumn")
elif user_month == 12 or user_month == 1 or user_month == 2:
    print("the season is winter")
                