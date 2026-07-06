import jwt
from datetime import datetime, timezone, timedelta
from functools import partial

from error_treatment.error import error_log_message

__all__ = ["create_token", "decode_token"]

KEY = "CHAVESECRETA"
ALG = "HS256"


def _base_create_token(KEY: str, alg: str, role: str = None, user_mail: str = None, user_id: int = None) -> dict:
    """
    Create a new token
    """
    try:


        if not role or not user_mail or not user_id:
            return {"Mensagem": "Dados para geração de token incompletos."}
        
        pay ={
        "role": role,
        "user_mail": user_mail,
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=120)
        }

        return {"token": (token := jwt.encode(
        payload= pay,
        algorithm= alg,
        key= KEY
        ))}
    
    except Exception as e:
        error_log_message(e)
        return {
            "messagem": "Erro na criação do token"
        }


def _base_decode_token(KEY: str, ALG: list, token: str = None) -> dict:
    """
    Decode and validate a token
    """
    try:

        if not token:
            return {"Mensagem": "Dados para decodificação do token incompletos"}
        
        payload = jwt.decode(token, key=KEY, algorithms= ALG)

        if not "role" in payload:
            return { "Mensagem": "fala na decodificação do payload."}

        return payload
    
    except jwt.InvalidTokenError as e:
        error_log_message(e)
        return {"mensagem" : "token invalido"}
    
    except Exception as e:
        error_log_message(e)
        return {
            "Mensagem": "Erro na decodificação do token"
        }

create_token = partial(_base_create_token, KEY, ALG)
decode_token = partial(_base_decode_token, KEY, ALG)


