from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./devicereader.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False, "echo": True})

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass