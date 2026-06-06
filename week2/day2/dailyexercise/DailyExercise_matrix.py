# ============================================================
#  Matrix Decoder – Decrypt a hidden message from a grid
# ============================================================

MATRIX_STR = '''
7ir
Tsi
h%x
i ?
sM# 
$a 
#t%'''

# ── Step 1: Transform the string into a 2D list (matrix) ────────────────────
# Split on newlines; skip the empty line produced by the leading newline.
# Each row becomes a list of individual characters.

matrix = []

for line in MATRIX_STR.split('\n'):
    if line:                          # ignore empty lines
        matrix.append(list(line))

print("2D Matrix:")
for row in matrix:
    print(row)

num_rows = len(matrix)
num_cols = len(matrix[0])

# ── Step 2: Process columns – build a flat character stream ─────────────────
# Neo reads the matrix column by column, top to bottom, left to right.
# We collect every character in that order into one flat list.

flat_chars = []

for col in range(num_cols):           # left column → right column
    for row in range(num_rows):       # top row → bottom row
        flat_chars.append(matrix[row][col])

print("\nFlat column-wise stream:", flat_chars)

# ── Steps 3 & 4: Filter alpha chars; replace symbol groups with one space ───
# Walk the flat stream character by character:
#   • Alpha character → keep it; add to the message.
#   • Non-alpha character (symbol, digit, space) that appears BETWEEN two alpha
#     characters → mark a "pending space" (the whole group collapses into one).
#
# The pending_space flag lets us insert exactly one space for any run of
# non-alpha characters, and only after we've already seen at least one letter.

decoded_message = ""
pending_space = False                 # True when a symbol gap awaits the next alpha

for char in flat_chars:
    if char.isalpha():                # Step 3: letter found – keep it
        if pending_space:
            decoded_message += " "   # Step 4: one space replaces the whole gap
            pending_space = False
        decoded_message += char
    else:                             # non-alpha character
        if decoded_message:           # only create a gap after the first letter
            pending_space = True

# ── Step 5: Print the decoded message ───────────────────────────────────────
print("\nDecoded message:", decoded_message)
