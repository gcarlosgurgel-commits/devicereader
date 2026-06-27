from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    """
    Defines the properties of users and their data type.
    """
    first_name: str
    last_name: str
    age: int
    mail: EmailStr


class ConsultarUser(BaseModel):
    user_mail: EmailStr