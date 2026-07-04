from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UserModel

from schemas.schemas import UserGenerateSchema, UserLoginSchema

from auth import jwt_handler
from core import security

from error_treatment.error import error_log_message

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


@router.post("/register")
def auth_register(data: UserGenerateSchema, db: Session = Depends(get_db)):  

    user = UserModel(
        first_name= data.first_name, 
        last_name= data.last_name, 
        user_age= data.age, 
        user_mail = data.mail,
        password_hash = security.password_hasher(data.password)
        )

    if (existing_user := db.query(UserModel).filter(UserModel.user_mail == data.mail).first()):
        #####CHECAR USER  E SENHA SERÁ REPETITIVO , MAKE IT DRY####
        return{
            "MensagemErro": "Usuário(a) já regitadoA(a)"
        }

    
    db.add(user)
    db.commit()
    db.refresh(user)

    existing_user = db.query(UserModel).filter(UserModel.user_mail == data.mail).first()
    token = jwt_handler.create_token("user", data.mail, existing_user.id) 

    return{
        "Mensagem":"Usuário registado com sucesso.",
        "Nome": f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
        "Age": user.user_age,
        "E-mail": user.user_mail,
        "token": {
            "access_token": token
        }
    }


@router.post("/login")
def auth_login(data: UserLoginSchema, db: Session = Depends(get_db)):

    try:
        if not (user_exists := db.query(UserModel).filter(UserModel.user_mail == data.email).first()):
            #####CHECAR USER  E SENHA SERÁ REPETITIVO , MAKE IT DRY####
            return {
                "mensagem": "usuário não encontrado. Verifique seu e-mail"
            }
        
        if not security.verify_password(data.password, user_exists.password_hash):
            #####CHECAR USER  E SENHA SERÁ REPETITIVO , MAKE IT DRY####
            return{
                "mensagem": "Login inválido"
            }
        
        #Cria o otken do usuário
        token = jwt_handler.create_token("user", data.email, user_exists.id)
        
        return{
            "mensagem": "bem vindo usuario",
            "token": token
        }
        
    except Exception as e:
        error_log_message(e)
        return {
            "messagem": "erro ao tentar efetuar login do usuário"
        }