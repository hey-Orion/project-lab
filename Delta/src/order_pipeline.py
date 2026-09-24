import sqlite3
import requests
from pydantic import BaseModel, ValidationError
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

