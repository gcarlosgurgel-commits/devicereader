from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User_db

from models import UserRequest

from auth import jwt_handler
from core import security

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def auth_register(data: UserRequest, db: Session = Depends(get_db)):  

    user = User_db(
        first_name= data.first_name, 
        last_name= data.last_name, 
        user_age= data.age, 
        user_mail = data.mail,
        password_hash = security.password_hasher(data.password)
        )

    if (existing_user := db.query(User_db).filter(User_db.user_mail == data.mail).first()):
        return{
            "MensagemErro": "Usuário(a) já regitadoA(a)"
        }

    
    db.add(user)
    db.commit()
    db.refresh(user)

    token = jwt_handler.create_token("user") 

    return{
        "Mensagem":"Usuário registado com sucesso.",
        "Nome": f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
        "Age": user.user_age,
        "E-mail": user.user_mail,
        "token": {
            "access_token": token
        }
    }