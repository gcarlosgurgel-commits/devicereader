from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.schemas import DeviceGenerateSchema
from database.database import get_db
from database.models import DeviceModel
from hardware.device import Device

from auth import jwt_handler
from core.security import oauth_scheme

from error_treatment import error

router= APIRouter(prefix="/devices", tags=["devices"])

def get_current_user(token: str = Depends(oauth_scheme)):

    #pegar o payload do token
    payload = jwt_handler.decode_token(token)

    #Verificar se token está valido
    if not "role" in payload.keys():
        return None
    
    return payload
    

@router.post("/generate")
def devices_generate(data: DeviceGenerateSchema, db: Session = Depends(get_db), token: any = Depends(oauth_scheme)) -> dict:
    try:

        #Ferificar se há Data
        if not data:
            return {"Mensagem": "Não foram enviados os dados solicitados para registo do dispositivo."}
        
        #Verifica se já ha dispositivo com o mesmo nome
        device_name = data.device_name
        if (device_exists := db.query(DeviceModel).filter(DeviceModel.alias == device_name).first()):
            return {"Mensagem": "Já existe um dispositivo com o mesmo nome. Escolha outro nome para seu novo dispositivo."}

        #Verificar se ha token
        if not token:
            return {"Mensagem": "Não há token de acesso válido."}

        #Pegar informacoes do usuario a partir do token recebido
        payload = jwt_handler.decode_token(token)

        #Verifica se foi retornado dados truthy no payload
        if not payload:
            return {"Mensagem": "Falha no processamento dos dados de acesso [Token]."}

        #Verificar se token do usuario esta válido verificando a presença de claims geralmente presentes no payload
        if not "role" in payload.keys():
            return {
                "Mensagem": "Token invalido. Usuário deslogado"
            }

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
            "messagem": "Dispositivo escaneado com sucesso",
            "Disposito": device_instance
        }
    
    except Exception as e:
        error.error_log_message(e)
        return {
            "Mensagem": "Erro ao gerar novo dispositivo "
        }
    

@router.get("/list")
def list_devices(db: Session = Depends(get_db),payload: any = Depends(get_current_user)) -> dict:
    try:
        if not payload:
            return {"Messagem": "Acesso não validado"}

        #Verificar se há dispositivos
        query = db.query(DeviceModel).filter(DeviceModel.user_id == payload["user_id"]).all()
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
                    "UserName": device.username,
                }
            )

        return {"Mensagem": lista}
    
    except Exception as e:
        error.error_log_message(e)
        return {
            "messagem": "Erro ao listar dispositivos do usuário"
        }
    
