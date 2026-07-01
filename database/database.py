from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///./devicereader.db", echo=True, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)