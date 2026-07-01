from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from user.user import User
from models import UserRequest, ConsultarUser

from database import models
from database.database import engine, SessionLocal

from hardware.cpu import CPU
from hardware.memory import Memory
from hardware.device import Device


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#GET Routes

@app.get("/")
def root():
    """
    returns wellcome message
    """
    return {"Mensagem": "Bem vindo ao app ReaderDevice."}

@app.get("/contacts")
def contacts():
    """
    Returns DeviceReaders contacts
    """
    return{
        "email": "devicereader@dr.com",
        "Tlm": "+351 968829644"
    }

@app.get("/users")
def users():
    """
    Returns options relationeted to Users
    """
    return {
        "mensagem": "O que deseja fazer?",
        "Option 1": "Criar novo usuário",
        "Option 2": "Consultar usuário",
        "Option 3": "Alterar dados do usuário",
        "Option 4": "Excluir usuário"
    }

@app.get("/devices")
def deviceRoot():
    """
    Returns options relationeted to Device
    """
    return {
        "mensagem": "O que deseja fazer?",
        "Option 1": "Escanear um novo dispositivo",
        "Option 2": "Consultar dados de um dispositivo",
        "Option 3": "Deletar dados de um dispositivo"
    }

@app.get("/devices/scan")
def deviceScan():
    """
    Scan the current device
    """

    return {
        "Mensagem": "Dispositivo escaneado com sucesso.",
        "Device": Device().get_general_information(),
        "cpu": CPU().get_general_information(),
        "memory": Memory().get_general_information()

    }

#POST Routes **Falta persistir tudo em banco de dados**

@app.post("/users/create")
def create_user(data: UserRequest, db: Session = Depends(get_db)):
    """
    Receive data
    Check data
    persist data in Db
    """

    usuario = models.User(first_name= data.first_name, last_name = data.last_name, user_age = data.age, user_mail = data.mail)

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return {
        "Message": "Usuário criado com sucesso",
        "first_name": usuario.first_name,
        "last_name": usuario.last_name,
        "user_age": usuario.user_age,
        "user_mail": usuario.user_mail
    }

@app.post("/users/consultar")
def consutar_user(data: ConsultarUser):
    """
    - Check permission;
    - Receive user mail;
    - Check if its exist in DB
    - If yes, return the datas to.
    """
    email = data.user_mail

    return {
        "Mensagem": f"Em breve retornaremos os dados de {email}. Obrigado"
    }

#PUT Routes **Falta persistir tudo em banco de dados**
