# ╔══════════════════════════════════════════════════════╗
# ║   JSON HANDLING TEMPLATE                             ║
# ╚══════════════════════════════════════════════════════╝

import json

data = {"a": 1, "b": 2}
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)


# ╔══════════════════════════════════════════════════════╗
# ║   FILE HANDLING TEMPLATE                             ║
# ╚══════════════════════════════════════════════════════╝

try:
    with open("file.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("File not found!")


# ╔══════════════════════════════════════════════════════╗
# ║   CSV HANDLING TEMPLATE                              ║
# ╚══════════════════════════════════════════════════════╝

import csv

# Writing to CSV
rows = [
    ["name", "age"],
    ["John", 30],
    ["Alice", 25],
]

with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Reading from CSV
try:
    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
except FileNotFoundError:
    print("CSV file not found!")
