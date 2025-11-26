
# database.py

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from contextlib import asynccontextmanager
import uvicorn
import csv
import io

print("""
2222222222222222222222222222222222
2222222222222222222222222222222222
2222222222222222222222222222222222
""")
# ============================================================================
# Database Configuration
# ============================================================================

sqlite_file_name = "Soldier_db.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)


# ============================================================================
# SQLModel Models
# ============================================================================

class SoldierBase(SQLModel):
    Soldier_id: int                                 # personal_id -> all start with 8 and have a len of 7
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    gender: str = Field(index=True)
    lives_at: str
    distasnce: int

# assign default "waiting" upon creation
class SoldierCreate(SoldierBase):
    state:str = "waiting"

class SoldierUpdate(SQLModel):
    state:str = "waiting"
    lives_at: str


class Soldier(SoldierBase, table=True):
    id: int | None = Field(default=None, primary_key=True)    

class SoldierRead(SQLModel):
    id: int 
    Soldier_id: int                                
    first_name: str 
    last_name: str 
    gender: str 
    lives_at: str
    distasnce: int
    state:str

# --- Dorms Models ---

class DormBase(SQLModel):
    name: str   # Dorm 1,Dorm 2
    
class DormCreate(DormBase):
    rooms: int = 10

class DormUpdate(SQLModel):
    pass

class Dorm(DormBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class DormRead(SQLModel):
    id: int 
    name: str   
    rooms: int

# --- Room Models ---

class RoomBase(SQLModel):
    slots: int = 0

class RoomCreate(RoomBase):
    slots: int = 8

class RoomUpdate(SQLModel):
    slots: int 

class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class DormRead(SQLModel):
    id: int 
    slots: int



# ============================================================================
# Database Initialization
# ============================================================================

def init_db():
    print("""
    44444444444444444444444444444444444444444
    444444444444444444444444444444444444444444
    444444444444444444444444444444444444444444
    """)

    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)

    print("""
    555555555555555555555555555555555555555555555555
    555555555555555555555555555555555555555555555555
    555555555555555555555555555555555555555555555555
        """)


# ============================================================================
# Dependency: Database Session
# ============================================================================

def get_session():
    """
    Dependency function that provides a database session.
    FastAPI will call this for each request that needs database access.
    The session is automatically closed after the request.
    """
    with Session(engine) as session:
        yield session



# ============================================================================
# Helper (Controller) Functions for Database Operations
# ============================================================================

def read_Soldier(session: Session) -> list[Soldier]:
    """Read Soldier from database"""
    statement = select(Soldier)  
    Soldier = session.exec(statement).all()
    return Soldier


def get_Soldier_by_id(session: Session, Soldier_id: int) -> Soldier | None:
    """Get a single Soldier by ID"""
    return session.get(Soldier, Soldier_id)

def create_Soldier_in_db(session: Session, Soldier: SoldierCreate) -> Soldier:
    """Create a new Soldier in database"""
    # Create Soldier instance from SoldierCreate
    db_Soldier = Soldier(
        Soldier_id=Soldier.Soldier_id,
        first_name=Soldier.first_name,
        last_name=Soldier.last_name,
        gender=Soldier.gender,
        lives_at=Soldier.lives_at,
        distasnce=Soldier.distasnce,
        state="waiting"
    )
    
    # Add to session and commit
    session.add(db_Soldier)
    session.commit()
    session.refresh(db_Soldier)  # Refresh to get the generated ID
    
    return db_Soldier


def update_Soldier_assigned(session: Session, Soldier_id: int, Soldier_update: SoldierUpdate) -> Soldier:
    """Update an existing Soldier in database"""
    Soldier = session.get(Soldier, Soldier_id)
    if not Soldier:
        raise HTTPException(status_code=404, detail="Soldier not found")
      
    # Update to "assigned"
    Soldier.status = "assigned"
    
    session.add(Soldier)
    session.commit()
    session.refresh(Soldier)
    
    return Soldier


def delete_Soldier_from_db(session: Session, Soldier_id: int) -> bool:
    """Delete a Soldier from database"""
    Soldier = session.get(Soldier, Soldier_id)
    if not Soldier:
        raise HTTPException(status_code=404, detail="Soldier not found")
    
    session.delete(Soldier)
    session.commit()
    return True


def delete_all_Soldier_from_db(session: Session):
    """Delete all Soldier from database"""
    statement = select(Soldier)
    Soldier = session.exec(statement).all()
    
    for Soldier in Soldier:
        session.delete(Soldier)
    
    session.commit()


def import_csv_to_db(session: Session, csv_content: bytes) -> dict:
    """Import CSV content and append rows to Soldier table. CSV file is not stored."""
    try:
        # Parse CSV
        csv_text = csv_content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        
        imported_count = 0
       
        # Append rows to Soldier table
        for row in csv_reader:
            title = row.get('title', '').strip()
            if not title:  # Skip rows without title
                continue
            
            # Create Soldier using SQLModel
            Soldier = Soldier(
                first_name=row.get('first_name', '').strip(),
                last_name=row.get('last_name', '').strip(),
                gender=row.get('gender', '').strip(),
                lives_at=row.get('lives_at', '').strip(),
                distasnce=int(row.get('distasnce', 0)),
            )
            
            session.add(Soldier)
            imported_count += 1
        
        session.commit()
        
        return {
            "message": f"Successfully imported {imported_count} Soldier from CSV",
            "imported_count": imported_count,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error importing CSV: {str(e)}")