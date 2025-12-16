#Write code that asks the user for a number and determines whether this number is odd or even.
num = int(input("choose a number: "))

if num % 2 == 0:
    print(f"the number {num} is even")
else:
    print(f"the number {num} is not even")
