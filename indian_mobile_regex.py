import re

# Read text from file
with open("data.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Regex pattern for valid 10-digit Indian mobile numbers
pattern = r"\b[6-9]\d{9}\b"

# Extract mobile numbers
numbers = re.findall(pattern, text)

# Display results
print("Valid Indian Mobile Numbers:")
for number in numbers:
    print(number)
