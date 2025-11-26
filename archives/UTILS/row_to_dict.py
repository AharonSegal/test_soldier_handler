#row_to_dict
# util to conver a row to dict

import sqlite3
from typing import List

#no bools
def row_to_dict(row: sqlite3.Row) -> dict:
    """
    Convert a generic SQLite row (sqlite3.Row) to a dictionary.
    This works by iterating over the column names available in the row object.
    """
    # row.keys() returns a list of column names for the current row
    # which is exactly what we need for the dictionary keys.
    # The dictionary comprehension builds the dict dynamically.
    return {col: row[col] for col in row.keys()}


# Define the columns that should be treated as Booleans (1 or 0 in the DB)
# In a real application, this list would often be a global constant or a class attribute.
BOOLEAN_COLUMNS: List[str] = ['is_active', 'is_verified', 'is_owner'] 


def row_to_dict_with_bools(row: sqlite3.Row) -> dict:
    """
    Converts an sqlite3.Row object to a dictionary.
    
    It dynamically converts integer values (1 or 0) in predefined 
    BOOLEAN_COLUMNS back into Python True or False.
    """
    result = {}
    
    # 1. Iterate over all column names available in the fetched row object.
    for col_name in row.keys():
        
        # 2. Retrieve the value for the current column.
        value = row[col_name]
        
        # 3. Check if the current column is one of the designated Boolean columns.
        if col_name in BOOLEAN_COLUMNS:
            # 4. If it is a Boolean column, use Python's bool() constructor.
            #    - bool(1) evaluates to True
            #    - bool(0) evaluates to False
            #    - This correctly converts the SQLite integer (1/0) back to a Python bool.
            result[col_name] = bool(value)
        else:
            # 5. For all other columns (strings, ints, floats, etc.), the value is 
            #    assigned directly without modification.
            result[col_name] = value
            
    return result