"""
pip install fastapi
pip install pydantic
pip install 'pydantic[email]'
pip install SQLAlchemy
pip install sqlmodel
pip install uvicorn
pip install requests
pip install python-dotenv
"""

# ---------------------------------------
#  Standard Library (built into Python)
# ---------------------------------------

import os
import sys
import json
import datetime
import pathlib
import logging

# Extra commonly used imports
from pathlib import Path                # Object-oriented filesystem paths
from logging import getLogger           # Quick logger access
from datetime import timedelta, date     # Useful time objects


# ---------------------------------------
#  Databases
# ---------------------------------------

import sqlite3
import sqlalchemy
import sqlmodel

# Common SQLAlchemy imports
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    select,
)

from sqlalchemy.orm import (
    Session,
    declarative_base,
    relationship,
)

# SQLModel essentials
from sqlmodel import (
    SQLModel,
    Field,
    Session as SQLSession,
    create_engine,
)


# ---------------------------------------
#  Web & APIs
# ---------------------------------------

import requests
from fastapi import FastAPI

# Common requests helpers
from requests import Session as RequestSession

# Typical FastAPI imports
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

# ---------------------------------------
#  Pydantic & Validation
# ---------------------------------------

from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError
from typing import Optional, List, Dict
from datetime import datetime

# ---------------------------------------
#  Environment & Configuration
# ---------------------------------------

from dotenv import load_dotenv
import configparser

# Typical configparser helpers
from configparser import ConfigParser

# ---------------------------------------
#  Utilities
# ---------------------------------------

import functools
import itertools
import random

# Convenient direct imports
from functools import lru_cache, partial
from itertools import groupby, chain
from random import randint, choice
