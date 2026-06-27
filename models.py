from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    user_mail: EmailStr


class DeviceRequest(BaseModel):
    name: str
    user_id: int

clas