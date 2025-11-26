from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException, status
import csv
import io


from .models import Soldier, SoldierCreate, SoldierUpdate
from .database import get_session
from .models import get_current_time_iso


"""    
🚨 IMPORTANT 🚨
CSV modifyed and changed column names
ps,first_name,last_name,gender,lives_at,distasnce


ps (personal_id): int -> all start with 8 and have a len of 7
    first_name: str -> first name
    last_name: str  -> last name
    gender: str     -> male or female (not a bool field)
    lives_at: str   -> soldiers home
    distasnce: int  -> distance from base
"""

def import_Soldiers_from_csv(csv_content: bytes, session: Session) -> dict:
    """Import Soldiers from CSV."""
    csv_text = csv_content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    
    imported_count = 0
    
    for row in csv_reader:
        try:
            # Prepare data, using Pydantic validation
            owner_data = SoldierCreate(
                first_name=row.get('first_name', '').strip(),
                last_name=row.get('last_name', '').strip(),
                gender=row.get('gender', '').strip(),
                lives_at=row.get('lives_at', '').strip(),
                distasnce=int(row.get('distasnce', 0)),
            )
            
            # Create the SQLModel instance and add to session
            db_owner = Soldier.model_validate(owner_data)
            
            session.add(db_owner)
            session.flush() # Commit immediately to catch unique constraint errors
            imported_count += 1
            
        except Exception:
            session.rollback()
            continue # Skip invalid rows or duplicates

    session.commit()
    return {
        "message": f"Successfully imported {imported_count} Soldiers from CSV",
        "imported_count": imported_count,}

