# ============================================================
#  Week 2 Day 4 — Exercise 1 & Exercise 2
# ============================================================
import random
import sys
import json

FILE_PATH = r"C:\Users\USER\Downloads\words.zip\words.txt"


# ============================================================
#  Exercise 1: Random Sentence Generator
# ============================================================

def get_words_from_file(file_path):
    """Read a word file and return a list of words."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
        words = content.split()
        return words
    except FileNotFoundError:
        print(f"Error: the file '{file_path}' was not found.")
        sys.exit(1)


def get_random_sentence(length):
    """Generate a random sentence of `length` words from the word file."""
    words = get_words_from_file(FILE_PATH)
    chosen = [random.choice(words) for _ in range(length)]
    sentence = " ".join(chosen)
    sentence = sentence.lower()
    return sentence


def run_exercise1():
    print("=== Exercise 1: Random Sentence Generator ===\n")

    user_input = input("How many words would you like? (2–20): ")

    try:
        length = int(user_input)
    except ValueError:
        print("Error: please enter a whole number.")
        sys.exit(1)

    if not (2 <= length <= 20):
        print("Error: the number must be between 2 and 20 inclusive.")
        sys.exit(1)

    sentence = get_random_sentence(length)
    print(f"\nYour random sentence:\n{sentence}")


# ============================================================
#  Exercise 2: Working with JSON
# ============================================================

def run_exercise2():
    print("\n=== Exercise 2: Working with JSON ===\n")

    # The raw JSON string given in the assignment
    sample_json = """{
   "company":{
      "employee":{
         "name":"emma",
         "payable":{
            "salary":7000,
            "bonus":800
         }
      }
   }
}"""

    # Step 1: Parse the JSON string into a Python dictionary
    data = json.loads(sample_json)

    # Step 2: Access the nested "salary" key
    salary = data["company"]["employee"]["payable"]["salary"]
    print(f"Employee salary: {salary}")

    # Step 3: Add a "birth_date" key to the employee dict
    data["company"]["employee"]["birth_date"] = "1995-06-15"
    print(f"Birth date added: {data['company']['employee']['birth_date']}")

    # Step 4: Save the modified dictionary to a JSON file
    output_file = "employee_data.json"

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nModified JSON saved to '{output_file}'")

    print("\n--- Contents of saved file ---")
    with open(output_file, "r") as f:
        print(f.read())


# ============================================================
#  Main — run both exercises
# ============================================================

if __name__ == "__main__":
    run_exercise1()
    run_exercise2()
