from pydantic import BaseModel, EmailStr, field_validator

class UserRequest(BaseModel):
    """
    Defines the properties of users and their data type.
    **
    first_name:,
    last_name,
    age,
    mail,
    """
    first_name: str
    last_name: str
    age: int
    mail: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_passord(cls, value):
        if len(value) < 8:
            raise ValueError("Password deve ter no mínimo 8 caracteres")
        if not any(c.isupper() for c in value):
            raise ValueError("Password deve ter pelo menos uma letra maiúscula")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password deve ter pelo menos um número")
        if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in value):
            raise ValueError("Password deve ter pelo menos um caractere especial")
        return value