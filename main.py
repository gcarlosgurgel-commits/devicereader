from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database.database import engine, SessionLocal
from database import models


from user.user import User
from hardware.cpu import CPU
from hardware.memory import Memory

from models import UserRequest


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "DeviceReader API funcionando"}

@app.post("/users")
def create_user(data: UserRequest, db: Session = Depends(get_db)):

    user = models.User(
        first_name=data.first_name,
        last_name=data.last_name,
        user_mail=data.user_mail
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "full_name": f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
        "user_mail": user.user_mail,
        "created_at": user.created_at
    }

@app.get("/hardware")
def get_hardware_info():
    cpu = CPU()
    ram = Memory()
    return{
        "cpu": cpu.get_general_information(),
        "memory": ram.get_general_information()
    }