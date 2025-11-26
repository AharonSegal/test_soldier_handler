import sqlite3
import csv
from datetime import datetime
import os # Added for path normalization

DB_FILE = "car_owners_db.db"
# Ensure the path is correct regardless of OS for robustness
CSV_FILE = os.path.join("full_exercise_easy", "sample_car_owners.csv") 
TABLE_NAME = "car_owners"

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Get the current ISO timestamp once
current_timestamp = datetime.now().isoformat()

# --- 1. Dynamic Table Creation ---

# Read the first row of CSV to get column names
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # first row is headers
    
# Determine if we need to auto-populate the timestamp
# NOTE: The header must match exactly (e.g., 'created_at')
needs_timestamp_injection = 'created_at' in headers

# Build CREATE TABLE query dynamically
# We use a set of headers for the CREATE statement.
columns_sql = ", ".join([f'"{col}" TEXT' for col in headers])  # all columns as TEXT
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    {columns_sql}
)
"""
cursor.execute(create_table_sql)


# --- 2. Dynamic Data Insertion ---

print(f"Starting import from {CSV_FILE}...")

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # maps columns automatically
    
    # Pre-calculate the SQL components once for efficiency
    placeholders = ", ".join([f":{col}" for col in headers])
    insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(headers)}) VALUES ({placeholders})"

    for row in reader:
        # Check if the 'created_at' field exists and is currently empty (or needs overwrite)
        if needs_timestamp_injection and not row.get('created_at'):
            # If the column exists in the CSV headers, inject the current timestamp
            # This ensures that even if the column is present but empty in the CSV, 
            # it gets populated upon import.
            row['created_at'] = current_timestamp
        
        try:
            # The 'row' dictionary contains all necessary values for the SQL insertion
            cursor.execute(insert_sql, row)
        except sqlite3.IntegrityError as e:
            # Handle cases like UNIQUE constraints (e.g., duplicate email)
            print(f"Skipping row due to integrity error: {e}. Data: {row}")
        except Exception as e:
            # Handle other insertion errors
            print(f"An error occurred during insertion: {e}. Data: {row}")

conn.commit()
conn.close()

print(f"CSV '{CSV_FILE}' imported successfully into '{DB_FILE}' as table '{TABLE_NAME}'")
print(f"Timestamp injection: {'ACTIVE' if needs_timestamp_injection else 'INACTIVE (created_at field not found)'}")