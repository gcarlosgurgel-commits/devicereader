from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

# Cria a conexão com o banco SQLite — o engine é a infraestrutura base
engine = create_engine(
    "sqlite:///./devicereader.db", 
    echo=True, 
    connect_args={"check_same_thread": False}
    )

# Fábrica de sessões — cada requisição vai abrir e fechar a sua própria sessão
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """
    Função que abre a sessão e encerra.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
