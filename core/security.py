from pwdlib import PasswordHash
from error_treatment.error import error_log_message



def password_hasher(password:str) -> str:
    """
    Faz o hash do password
    """
    try:
        password_hash = PasswordHash.recommended()
        hashed_password = password_hash.hash(password)
        return hashed_password
    except Exception as e:
        error_log_message(e)
        return {"[ERROR]": "Erro no hash do password."}
    

def verify_password(password, hashed_password):
    """
    Faz o check do password
    """
    try:
        password_hash = PasswordHash.recommended()
        is_valid = password_hash.verify(password, hashed_password)
        return is_valid
    except Exception as e:
        error_log_message(e)
        return {"[ERROR]": "Erro no hash do password."}
    