import numpy as np

# ============================================================
# Exercise 1: Array Creation and Manipulation
# Create a 1D NumPy array containing numbers from 0 to 9.
# ============================================================
print("=" * 50)
print("Exercise 1: Array Creation and Manipulation")
print("=" * 50)
arr1 = np.arange(10)
print(repr(arr1))
print()

# ============================================================
# Exercise 2: Type Conversion and Array Operations
# Convert a list [3.14, 2.17, 0, 1, 2] into a NumPy array
# and convert its data type to integer.
# ============================================================
print("=" * 50)
print("Exercise 2: Type Conversion and Array Operations")
print("=" * 50)
arr2 = np.array([3.14, 2.17, 0, 1, 2]).astype(int)
print(repr(arr2))
print()

# ============================================================
# Exercise 3: Working with Multi-Dimensional Arrays
# Create a 3x3 NumPy array with values ranging from 1 to 9.
# ============================================================
print("=" * 50)
print("Exercise 3: Working with Multi-Dimensional Arrays")
print("=" * 50)
arr3 = np.arange(1, 10).reshape(3, 3)
print(repr(arr3))
print()

# ============================================================
# Exercise 4: Creating Multi-Dimensional Array with Random Numbers
# Create a 2D NumPy array of shape (4, 5) filled with random numbers.
# ============================================================
print("=" * 50)
print("Exercise 4: Multi-Dimensional Array with Random Numbers")
print("=" * 50)
np.random.seed(42)  # Seed for reproducibility
arr4 = np.random.rand(4, 5)
print(np.array2string(arr4, formatter={'float_kind': lambda x: f"{x:.2f}"}))
print()

# ============================================================
# Exercise 5: Indexing Arrays
# Select the second row from the given 2D NumPy array.
# ============================================================
print("=" * 50)
print("Exercise 5: Indexing Arrays")
print("=" * 50)
array = np.array([[21, 22, 23, 22, 22],
                  [20, 21, 22, 23, 24],
                  [21, 22, 23, 22, 22]])
second_row = array[1]
print(repr(second_row))
print()

# ============================================================
# Exercise 6: Reversing Elements
# Reverse the order of elements in a 1D NumPy array.
# ============================================================
print("=" * 50)
print("Exercise 6: Reversing Elements")
print("=" * 50)
arr6 = np.arange(10)
arr6_reversed = arr6[::-1]
print(repr(arr6_reversed))
print()

# ============================================================
# Exercise 7: Identity Matrix
# Create a 4x4 identity matrix using NumPy.
# ============================================================
print("=" * 50)
print("Exercise 7: Identity Matrix")
print("=" * 50)
arr7 = np.eye(4)
print(repr(arr7))
print()

# ============================================================
# Exercise 8: Simple Aggregate Functions
# Find the sum and average of a given 1D array.
# ============================================================
print("=" * 50)
print("Exercise 8: Simple Aggregate Functions")
print("=" * 50)
arr8 = np.arange(10)  # [0, 1, 2, ..., 9]
total = arr8.sum()
average = arr8.mean()
print(f"Sum: {int(total)}, Average: {average}")
print()

# ============================================================
# Exercise 9: Create Array and Change its Structure
# Create a NumPy array with elements from 1 to 20;
# then reshape it into a 4x5 matrix.
# ============================================================
print("=" * 50)
print("Exercise 9: Create Array and Change its Structure")
print("=" * 50)
arr9 = np.arange(1, 21).reshape(4, 5)
print(repr(arr9))
print()

# ============================================================
# Exercise 10: Conditional Selection of Values
# Extract all odd numbers from a given NumPy array.
# ============================================================
print("=" * 50)
print("Exercise 10: Conditional Selection of Values")
print("=" * 50)
arr10 = np.arange(1, 10)  # [1, 2, 3, ..., 9]
odd_numbers = arr10[arr10 % 2 != 0]
print(repr(odd_numbers))
print()
