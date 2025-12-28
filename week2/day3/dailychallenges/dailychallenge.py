#Here is a python code that generates a list of 20000 random numbers, called list_of_numbers, and a target number.

import random

list_of_numbers = [random.randint(0, 10000) for _ in range(20000)]

target_number   = 3728


#Copy this code, and create a program that finds, within list_of_numbers all the pairs of number that sum to the target number

def find_the_pairs(numbers, target):
    pairs = []
    seen_num = {}

    for number in numbers:
        sum = target - number
        if seen_num.get(sum, 0) > 0:
            pairs.append((sum, number))
            seen_num[sum] -= 1
        seen_num[number] = seen_num.get(number, 0) + 1

    return pairs

pairs_found = find_the_pairs(list_of_numbers, target_number)

for a, b in pairs_found:
    print(f"{a} and {b} sum the target number {target_number}")

    


