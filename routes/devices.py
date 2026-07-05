from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from schemas.schemas import DeviceGenerateSchema
from database.database import get_db
from database.models import DeviceModel
from hardware.device import Device

from auth import jwt_handler

from error_treatment import error

router= APIRouter(prefix="/devices", tags=["devices"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/generate")
def devices_generate(data: DeviceGenerateSchema, db: Session = Depends(get_db), token: str = Depends(oauth_scheme)):
    try:

        ##Verificar se usuario esta logado
        #Como? O oauth faz isso automaticamente?

        ##Pegar id do usuario
        payload = jwt_handler.decode_token(token)

        #Escanear dispositivo
        device = Device()
        device_scanned = device.get_general_information()

        #Criar instancia de device na tabela do db
        device_instance = DeviceModel(
            alias= data.device_name,
            model= device_scanned["Model"], 
            name= device_scanned["Name"], 
            username = device_scanned["UserName"], 
            primaryOwnerName= device_scanned["PrimaryOwnerName"], 
            machine_id = device_scanned["MachineId"],
            user_id = payload["user_id"]
            )
        
        db.add(device_instance)
        db.commit()
        db.refresh(device_instance)

        return {
            "message": device_instance
        }
    except Exception as e:
        error.error_log_message(e)
        return {
            "Mensagem": "Erro ao gerar novo dispositivo "
        }
    

@router.get("/list")
def list_devices(db: Session = Depends(get_db),token: str = Depends(oauth_scheme)) -> dict:
    try:
        #pegar o payload do token
        user_token = jwt_handler.decode_token(token)

        #Verificar se token está valido
        if token["mensagem"].lower() == "token invalido":
            return {"Mensagem": "Token invalido"}

        #Verificar se há dispositivos
        query = db.query(DeviceModel).filter(DeviceModel.user_id == user_token["user_id"]).all() #query é um objeto lazy que so entrega conforme o solicitado.

        #Caso nao haja dispositivo
        if not query:
            return {"Mensagem": "Não há dispositivos a serem listados,"}
        

        lista = []
        for device in query:
            lista.append(
                {
                    "Alias": device.alias,
                    "Model": device.model,
                    "PrimaryOwnerName": device.primaryOwnerName,
                    "Name": device.name,
                    "User_id": device.user_id,
                    "UserName": device.username
                }
            )

        return {"Mensagem": lista}
    
    except Exception as e:
        error.error_log_message(e)
        return {
            "messagem": "Erro ao listar dispositivos do usuário"
        }