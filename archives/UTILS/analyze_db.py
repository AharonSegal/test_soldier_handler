"""
analyze_db_sqlite.py
utility -> testing the connection from python to the DATABASE_NAME (SQLite)
"""

from sqlmodel import Session, create_engine, SQLModel, select
import sqlite3
import os
from typing import List

# --- CONFIGURATION for SQLite ---
# Using a relative path for the SQLite database file
DB_FILE = "car_owners_db.db" 
DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, echo=False)

def get_sqlite_connection():
    """Helper function to establish standard sqlite3 connection."""
    if not os.path.exists(DB_FILE):
        print(f"Warning: Database file '{DB_FILE}' not found. It will be created if tables are defined/used.")
    
    # Using sqlite3 to handle direct SQL commands and metadata queries
    conn = sqlite3.connect(DB_FILE)
    # Set row factory to sqlite3.Row for dictionary-like access (like MySQL's dictionary=True)
    conn.row_factory = sqlite3.Row 
    return conn

def analyze_database():
    print("\n==================== DATABASE ANALYSIS (SQLite) ====================\n")
    
    try:
        # ---- 1. Connect using sqlite3 for metadata ----
        conn = get_sqlite_connection()
        cursor = conn.cursor()

        # ---- 2. Database name (Always the file name for SQLite) ----
        dbname = DB_FILE

        # ---- 3. Count tables (using sqlite_master) ----
        # sqlite_master is the internal table that stores the schema definition
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        # sqlite3.Row objects act like dictionaries, but we can also access by index (name is the only column)
        table_names = [t['name'] for t in tables] 
        table_count = len(table_names)

        # ---- 4. Count total columns in all tables ----
        total_columns = 0
        for table in table_names:
             # PRAGMA table_info(table_name) is the SQLite way to get column details
            cursor.execute(f"PRAGMA table_info({table})")
            total_columns += len(cursor.fetchall())
        
        # Display summary
        print(f"Database File Name : {dbname}")
        print(f"Total Tables       : {table_count}")
        print(f"Total Columns      : {total_columns}\n")

        print("-----------------------------------------------------------")
        print("TABLE DETAILS")
        print("-----------------------------------------------------------\n")

        # ---- 5. For each table: count rows + columns + preview ----
        for table in table_names:
            
            # row count
            cursor.execute(f"SELECT COUNT(*) AS count FROM {table}")
            row_count = cursor.fetchone()["count"]

            # column count (using PRAGMA again for accuracy)
            cursor.execute(f"PRAGMA table_info({table})")
            col_count = len(cursor.fetchall())

            print(f"Table: {table}")
            print(f"  Rows     : {row_count}")
            print(f"  Columns  : {col_count}")

            # top 5 rows
            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            rows = cursor.fetchall()

            if rows:
                print("  Top 5 Rows:")
                for r in rows:
                    # Convert the sqlite3.Row object to a standard dict for cleaner printing
                    print(f"    {dict(r)}") 
            else:
                print("  Top 5 Rows: (empty table)")

            print("-" * 60)

        cursor.close()
        conn.close()

    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# ---- RUN DIRECTLY ----
if __name__ == "__main__":
    analyze_database()