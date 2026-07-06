from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UserModel

from schemas.schemas import UserGenerateSchema, UserLoginSchema

from auth import jwt_handler
from core.security import password_hasher, verify_password

from error_treatment.error import error_log_message



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def auth_register(data: UserGenerateSchema, db: Session = Depends(get_db)):  
    """
    Create a new User.
    """

    #Verificar se ha Data
    if not data:
        return {"Mensagem": "Dados para geração de registro incompletos."}
    
    #verificar se valor de db e truthy
    if not db:
        return {"Mensagem": "Fala na requisicao ao banco de dados"}
    
    user = UserModel(
        first_name= data.first_name, 
        last_name= data.last_name, 
        user_age= data.age, 
        user_mail = data.mail,
        password_hash = password_hasher(data.password)
        )

    #Checando se o usuario ja existe no banco de dados
    if (existing_user := db.query(UserModel).filter(UserModel.user_mail == user.user_mail).first()):
        #####CHECAR USER  E SENHA SERÁ REPETITIVO , MAKE IT DRY####
        return{
            "MensagemErro": "Usuário(a) já regitadoA(a)"
        }

    
    db.add(user)
    db.commit()
    db.refresh(user)

    #Getting user_id to insert in token payload.
    existing_user = db.query(UserModel).filter(UserModel.user_mail == data.mail).first()

    #Generate token
    if not existing_user.id:
        return {"Mensagem": "Não foi localizado ID do usuário em banco de dados para geração do token"}
    
    token = jwt_handler.create_token("user", data.mail, existing_user.id) 

    return{
        "Mensagem":"Usuário registado com sucesso.",
        "Nome": f"{user.get_fullName()}",
        "Age": user.user_age,
        "E-mail": user.user_mail,
        "token": {
            "access_token": token
        }
    }


@router.post("/login")
def auth_login(data: UserLoginSchema, db: Session = Depends(get_db)):

    try:

        #Verificar se ha Data
        if not data:
            return {"Mensagem": "Dados para geração de registro incompletos."}
        
        #verificar se valor de db e truthy
        if not db:
            return {"Mensagem": "Fala na requisicao ao banco de dados"}

        #Verificando se o usuario ja existe em banco de dados
        if not (user_exists := db.query(UserModel).filter(UserModel.user_mail == data.email).first()):
            #####CHECAR USER  E SENHA SERÁ REPETITIVO , MAKE IT DRY####
            return {
                "mensagem": "usuário não encontrado. Verifique seu e-mail"
            }
        
        #Verificando se password esta correto
        if not verify_password(data.password, user_exists.password_hash):
            #####CHECAR USER  E SENHA SERÁ REPETITIVO , MAKE IT DRY####
            return{
                "mensagem": "Login inválido"
            }
        
        #Cria o token do usuário
        token = jwt_handler.create_token("user", data.email, user_exists.id)

        #Verifica se token foi criado com sucesso
        if not "token" in token.keys():
            return {"Mensagem": "Não foi possivel gerar o token de acesso para o usuário."}
        
        
        return{
            "mensagem": "bem vindo usuario",
            "token": token
        }
        
    except Exception as e:
        error_log_message(e)
        return {
            "messagem": "erro ao tentar efetuar login do usuário"
        }