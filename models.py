# Dorm_owner_api/models.py
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List


"""
each Dorm has 10 rooms
    has 10 rooms
each Room has 8 slots for 8 soldiers
    has 8 slots

Soldier
revived from csv:
    ps (personal_id): int -> all start with 8 and have a len of 7
    first_name: str -> first name
    last_name: str  -> last name
    gender: str     -> male or female (not a bool field)
    lives_at: str   -> soldiers home
    distasnce: int  -> distance from base

generated in code:
    state: str -> 2 options is_assigned or waiting (not a bool)

future improvments 
    make db ralational and have id od soldier in each room and each room id in each dorm

"""

# --- Soldier Models ---
# SoldierBase,SoldierCreate,SoldierUpdate,Soldier


class SoldierBase(SQLModel):
    ps: int                                 # personal_id -> all start with 8 and have a len of 7
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
    # Relationship: Define the link to the Dorm model
    Dorms: List["Dorm"] = Relationship(back_populates="owner")

class SoldierRead(SQLModel):
    id: int 
    ps: int                                
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
