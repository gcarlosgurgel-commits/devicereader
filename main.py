from fastapi import FastAPI
from database.models import Base
from database.database import engine
import uvicorn

from routes import auth, root, devices


app = FastAPI()
app.include_router(root.router)
app.include_router(auth.router)
app.include_router(devices.router)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload =True)
  