import sqlite3

DB_FILE = "car_owners_db.db"
TABLE_NAME = "cars"  # change to your table

def remove_duplicates():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get column names excluding the primary key
    cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
    columns = [col[1] for col in cursor.fetchall() if col[5] == 0]  # col[5]==1 is pk
    col_str = ", ".join(columns)

    # Delete duplicates keeping the lowest id
    cursor.execute(f"""
        DELETE FROM {TABLE_NAME}
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM {TABLE_NAME}
            GROUP BY {col_str}
        )
    """)
    conn.commit()

    # Count remaining rows
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    remaining = cursor.fetchone()[0]
    print(f"Duplicates removed. Table '{TABLE_NAME}' now has {remaining} rows.")

    conn.close()

if __name__ == "__main__":
    remove_duplicates()
