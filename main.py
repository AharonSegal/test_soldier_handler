from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from typing import List, Optional
from datetime import datetime
import csv
import io

DATABASE_URL = "sqlite:///Soldier_db.sqlite"
engine = create_engine(DATABASE_URL, echo=False)

app = FastAPI(title="Dorm Assignment API")

# --------------------
# Models
# --------------------

class DormBase(SQLModel):
    name: str
    rooms_count: int = 10  # default rooms per dorm

class Dorm(DormBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rooms: List["Room"] = Relationship(back_populates="dorm")


class RoomBase(SQLModel):
    number: int
    capacity: int = 8

class Room(RoomBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dorm_id: int = Field(foreign_key="dorm.id")
    dorm: Optional[Dorm] = Relationship(back_populates="rooms")
    soldiers: List["Soldier"] = Relationship(back_populates="room")


class SoldierBase(SQLModel):
    Soldier_id: int  # personal id (7 digits starting with 8)
    first_name: str
    last_name: str
    gender: str
    lives_at: Optional[str] = None
    distance: int = 0  # distance from base

class Soldier(SoldierBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    state: str = Field(default="waiting")  # waiting | assigned
    assigned_at: Optional[datetime] = None
    room_id: Optional[int] = Field(default=None, foreign_key="room.id")
    room: Optional[Room] = Relationship(back_populates="soldiers")


# --------------------
# DB init and helpers
# --------------------

def init_db():
    SQLModel.metadata.create_all(engine)
    # Create default dorms A and B with 10 rooms each if they don't exist
    with Session(engine) as session:
        dorms = session.exec(select(Dorm)).all()
        dorms_availble = ["Dorm A", "Dorm B"]
        if not dorms:
            # for each dorm -> will create it and make rooms for it 
            for dorm_name in dorms_availble:
                dorm = Dorm(name=dorm_name, rooms_count=10)
                session.add(dorm)
                session.commit()
                session.refresh(dorm)
                # create 10 rooms for rach dorm
                for num in range(1, 11):
                    room = Room(number=num, capacity=8, dorm_id=dorm.id)
                    session.add(room)
                session.commit()

# 🚨 THIS IS COMENTED OUT ONCE THE DB IS CREATED 🚨
# init_db()


# --------------------
# get_session
# --------------------

def get_session():
    with Session(engine) as session:
        yield session


# --------------------
# Validate_Soldier_id
# --------------------

def validate_Soldier_id_raw(value: str) -> int:
    """Validate a Soldier_id coming from CSV or payload.
       Rules: numeric, length 7, starts with '8'."""
    s = value.strip()
    if not s.isdigit():
        raise ValueError("Soldier_id must be numeric")
    if len(s) != 7:
        raise ValueError("Soldier_id must be 7 digits long")
    if not s.startswith("8"):
        raise ValueError("Soldier_id must start with '8'")
    return int(s)


# --------------------
# CSV import & endpoint
# --------------------

@app.post("/assignWithCsv")
async def assignWithCsv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """Upload a CSV file and append all rows to the todos table. Only appends to todos - CSV file is not stored."""
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    # Read file content
    contents = await file.read()
    
    # Import CSV and store in database
    result = import_csv_to_db(session, contents)
    
    return result



def import_csv_to_db(session: Session, csv_content: bytes) -> dict:
    """Import CSV content and append rows to soldiers table. CSV file is not stored."""
    
    try:
        # Parse CSV
        csv_text = csv_content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_text))
               
        # Append rows to todos table
        for row in csv_reader:   
       
            raw_id = row.get("Soldier_id", "").strip()
            # validates before assining
            Soldier_id = validate_Soldier_id_raw(raw_id)
            first_name = row.get("first_name", "").strip()
            last_name = row.get("last_name", "").strip()
            gender = row.get("gender", "").strip()
            lives_at = row.get("lives_at", "").strip()
            #  convert to int
            distance_raw = row.get("distance", "").strip()
            distance = int(distance_raw) 
               
            soldier = Soldier(
                Soldier_id=Soldier_id,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                lives_at=lives_at,
                distance=distance,
            )
            session.add(soldier)
            session.commit()
            session.refresh(soldier)

            print(f"""===========creating soldier ===- -======
                Soldier_id={Soldier_id},
                first_name={first_name},
                last_name={last_name},
                gender={gender},
                lives_at={lives_at},
                distance={distance},
                  """)
            
            session.add(soldier)
        
        session.commit()
        
        return {
            "message": f"Successfully imported  soldier from CSV",
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error importing CSV: {str(e)}")

# --------------------
# Assignment engine
# --------------------

# @app.post("/assign_waiting")
# async def assign_waiting(session: Session = Depends(get_session)):
#     result = assign_waiting(session) 
#     return result

# def assign_waiting(session: Session = Depends(get_session)):
#     """
#     Assign waiting soldiers to rooms based on distance -> desc
#     Fills rooms in dorm order -> Dorm A rooms 1, then Dorm B
#     """
#     # Get waiting soldiers sorted by distance desc (furthest first)
#     waiting_and_distance_filter = select(Soldier).where(Soldier.state == "waiting").order_by(Soldier.distance.desc())
#     waiting_soldiers: List[Soldier] = session.exec(waiting_and_distance_filter).all()

#     if not waiting_soldiers:
#         return {"assigned": 0, "message": "No waiting soldiers to assign."}

#     print(len(waiting_soldiers))

#     # Get all rooms and current occupancy
#     # dorm_id -> the room
#     # number -> what it can hold
#     rooms: List[Room] = session.exec(select(Room).order_by(Room.dorm_id, Room.number)).all()

#     print(rooms)
    
#     current_room = 0

#     #STUCK AT THIS STAGE
#     #TODO: CONTINUE AND COME BACK TO THIS 

#     for i in range(160):
#         print("=================SOLDIER============")
#         print(waiting_soldiers[i])
#         current_soldier = waiting_soldiers[i]
#         current_room = rooms[0]
#         # find first room with available slot
#         print("=================ROOM============")
#         print(current_room, "  -> ", current_room.capacity)
#         while current_room.capacity:
#             current_soldier.room_id = current_room.id
#             current_soldier.state = "assigned"

#             current_room.capacity -= 1

#             session.add(current_soldier)
#             session.add(current_room)
#             session.commit()
#             session.refresh(current_soldier)
#             session.refresh(current_room)

#     return 

# --------------------
# Count and List of waiting soldiers
# --------------------

@app.get("/waiting_soldiers")
def waiting_list(session: Session = Depends(get_session)):
    waiting = session.exec(select(Soldier).where(Soldier.state == "waiting")).all()    
    result = [
        {
            "db_id": soldier.id,
            "soldier_id": soldier.Soldier_id,
            "full_name": f"{soldier.first_name} {soldier.last_name}",
            "distance": soldier.distance
        }
        for soldier in waiting
    ]
    mesg = f"there are {len(result)} waiting to be assigned a room"
    return (mesg, result)









@app.post("/assign-waiting", summary="Assign waiting soldiers to rooms")
def assign_waiting(session: Session = Depends(get_session)):
    """
    Assign waiting soldiers to rooms based on distance (desc).
    Fills rooms in dorm order (Dorm A rooms 1.., then Dorm B).
    """
    # Get waiting soldiers sorted by distance desc (furthest first)
    waiting_stmt = select(Soldier).where(Soldier.state == "waiting").order_by(Soldier.distance.desc())
    waiting_soldiers: List[Soldier] = session.exec(waiting_stmt).all()

    if not waiting_soldiers:
        return {"assigned": 0, "message": "No waiting soldiers to assign."}

    # Get all rooms and current occupancy
    rooms: List[Room] = session.exec(select(Room).order_by(Room.dorm_id, Room.number)).all()

    # Build map room_id -> current_count
    room_capacity_map = {}
    for r in rooms:
        room_capacity_map[r.id] = {"room": r, "available": 8}

    print("ROOOOOM CAAAAPAACITTY")
    print(room_capacity_map)
    # {1: {'room': Room(capacity=0, dorm_id=1, number=1, id=1), 'available': 8}

    for soldier in waiting_soldiers:
        # find first room with available slot
        target_room_entry = None
        for idx,dic in room_capacity_map.items():
            if dic["available"] > 0:
                target_room_entry = dic
                break
        if not target_room_entry:
            # no more capacity
            break
        
        # assign soldier
        room_cur: Room = target_room_entry["room"]
        print(room_cur)
        soldier.room_id = room_cur.id
        soldier.state = "assigned"
        session.add(soldier)
        session.commit()
        session.refresh(soldier)

        # update room map
        target_room_entry["available"] -= 1

    return 

