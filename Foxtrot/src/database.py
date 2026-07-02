import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.sqlalchemy_models import Base

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_local = os.getenv("DATABASE_URL")

if not DATABASE_URL_local:
    raise ValueError("error") 

engine = create_engine(
    DATABASE_URL_local
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


Base.metadata.create_all(bind=engine)