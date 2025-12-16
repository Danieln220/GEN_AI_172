#Write code that will ask the user for their height in centimeters.
#If they are over 145 cm, print a message that states they are tall enough to ride.
#If they are not tall enough, print a message that says they need to grow some more to ride.

user_height = int(input("write your hight in centimeters please: "))

if user_height > 145:
    print("you are tall enough to ride")
else:
    print("you need to grow more to ride")    
