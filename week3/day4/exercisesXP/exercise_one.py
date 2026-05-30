import string
import random
from datetime import datetime
from faker import Faker
from week3.day4.exercisesXP.func import sum_two


# ── Exercise 1: Currencies ─────────────────────────────────────────────────────

class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount

    def __str__(self):
        return f'{self.amount} {self.currency}s'

    def __repr__(self):
        return f'{self.amount} {self.currency}s'

    def __int__(self):
        return int(self.amount)

    def __add__(self, other):
        if isinstance(other, int):
            return self.amount + other
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(
                    f'Cannot add between Currency type <{self.currency}> and <{other.currency}>'
                )
            return self.amount + other.amount
        raise TypeError(f'Unsupported type: {type(other)}')

    def __iadd__(self, other):
        if isinstance(other, int):
            self.amount += other
        elif isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(
                    f'Cannot add between Currency type <{self.currency}> and <{other.currency}>'
                )
            self.amount += other.amount
        else:
            raise TypeError(f'Unsupported type: {type(other)}')
        return self


c1 = Currency('dollar', 5)
c2 = Currency('dollar', 10)
c3 = Currency('shekel', 1)
c4 = Currency('shekel', 10)

print("── Exercise 1 ──")
print(c1)           # 5 dollars
print(int(c1))      # 5
print(repr(c1))     # 5 dollars
print(c1 + 5)       # 10
print(c1 + c2)      # 15
print(c1)           # 5 dollars

c1 += 5
print(c1)           # 10 dollars

c1 += c2
print(c1)           # 20 dollars

try:
    print(c1 + c3)
except TypeError as e:
    print(f'TypeError: {e}')


# ── Exercise 2: Import ─────────────────────────────────────────────────────────

print("\n── Exercise 2 ──")
sum_two(3, 7)       # 10


# ── Exercise 3: String module ──────────────────────────────────────────────────

print("\n── Exercise 3 ──")
letters = string.ascii_uppercase + string.ascii_lowercase
random_string = ''
for _ in range(5):
    random_string += random.choice(letters)
print(random_string)


# ── Exercise 4: Current Date ───────────────────────────────────────────────────

print("\n── Exercise 4 ──")
def show_current_date():
    today = datetime.now()
    print(today.strftime('%Y-%m-%d'))

show_current_date()


# ── Exercise 5: Time left until January 1st ────────────────────────────────────

print("\n── Exercise 5 ──")
def time_until_new_year():
    now = datetime.now()
    next_new_year = datetime(now.year + 1, 1, 1)
    time_left = next_new_year - now
    print(f'Time until January 1st: {time_left}')

time_until_new_year()


# ── Exercise 6: Birthday and minutes ──────────────────────────────────────────

print("\n── Exercise 6 ──")
def minutes_lived(birthdate_str):
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
    now = datetime.now()
    diff = now - birthdate
    minutes = int(diff.total_seconds() / 60)
    print(f'You have lived approximately {minutes:,} minutes!')

minutes_lived('1995-06-15')


# ── Exercise 7: Faker module ───────────────────────────────────────────────────

print("\n── Exercise 7 ──")
fake = Faker()
users = []

def add_users(count):
    for _ in range(count):
        user = {
            'name': fake.name(),
            'address': fake.address(),
            'language_code': fake.language_code()
        }
        users.append(user)

add_users(3)
for user in users:
    print(user)
