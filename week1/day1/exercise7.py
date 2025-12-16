
user_num = int(input('pick a number between 1 and 100: '))

if user_num % 15 == 0:
    print('fizzbuzz')

elif user_num % 3 == 0:
    print('fizz')

elif user_num % 5 == 0:
    print('buzz')