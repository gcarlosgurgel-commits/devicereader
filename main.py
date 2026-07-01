import uvicorn

from routes import app, root

aplication = app


if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload =True)
    



# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session

# from database.database import engine, SessionLocal
# from database import models


# # from user.user import User
# # from hardware.cpu import CPU
# # from hardware.memory import Memory

# from models import UserRequest, DeviceRequest


# app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/")
# def root():
#     """Return root endpoint message"""
#     return {"message": "Wellcome to your device reader."}

# @app.post("/create_user")
# def create_user(data: UserRequest, db: Session = Depends(get_db)):
#     """
#     Receive de datas send by client
#     persist the values in dataBase
#     Returns the users infor
#     """

#     user = models.User( 
#         first_name=data.first_name,
#         last_name=data.last_name,
#         user_age=data.age,
#         user_mail=data.user_mail
#     )

#     db.add(user) 
#     db.commit() 
#     db.refresh(user)
    
#     return {
#         # Returns the users information
#         "id": user.id,
#         "full_name": f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
#         "user_age": user.user_age,
#         "user_mail": user.user_mail,
#         "created_at": user.created_at
#     }

# # @app.get("/hardware")
# # def get_hardware_info():
# #     cpu = CPU()
# #     ram = Memory()
# #     return{
# #         "cpu": cpu.get_general_information(),
# #         "memory": ram.get_general_information()
# #     }


# # @app.post("/devices")
# # def create_device(data: DeviceRequest, db: Session = Depends(get_db)):
# #     user = db.query(models.User).filter(models.User.id == data.user_id).first()

# #     if not user:
# #         from fastapi import HTTPException
# #         raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
# #     device = models.Device ( 
# #         name = data.name,
# #         user_id= data.user_id 
# #         )

# #     db.add(device)
# #     db.commit()
# #     db.refresh(device)
# #     return{
# #         "id":device.id,
# #         "name": device.name,
# #         "user_id": device.user_id,
# #         "created_at": device.created_at
# #     }