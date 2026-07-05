import jwt
from datetime import datetime, timezone, timedelta
from functools import partial

from error_treatment.error import error_log_message

__all__ = ["create_token", "decode_token"]

KEY = "CHAVESECRETA"
ALG = ["HS256"]


def _base_create_token(KEY: str, alg: str, role: str, user_mail: str, user_id: int) -> dict:
    """
    Create a new token
    """
    try:
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


def _base_decode_token(KEY: str, ALG: list, token: str) -> dict:
    """
    Decode and validate a token
    """
    try:
        payload = jwt.decode(token, key=KEY, algorithms= ALG)
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


