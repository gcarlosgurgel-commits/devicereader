from fastapi import FastAPI
from pydantic import BaseModel

from user.user import User
from hardware.cpu import CPU
from hardware.memory import Memory


app = FastAPI()

class UserRequest(BaseModel):
    first_name: str
    last_name: str
    user_mail: str

@app.get("/")
def root():
    return {"message": "DeviceReader API funcionando"}

@app.post("/users")
def create_user(data: UserRequest):
    user = User(data.first_name, data.last_name, data.user_mail)
    return{
        "full_name": user.get_user_full_name(),
        "last_name": user.get_user_mail()
    }

@app.get("/hardware")
def get_hardware_info():
    cpu = CPU()
    ram = Memory()
    return{
        "cpu": cpu.get_general_information(),
        "memory": ram.get_general_information()
    }