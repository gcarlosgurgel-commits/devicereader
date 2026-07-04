from fastapi import APIRouter

router = APIRouter(tags=["root"])

@router.get("/")
def root():
    return {
        "Root": "Bem vindo a root"
    }