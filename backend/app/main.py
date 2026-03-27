from fastapi import FastAPI
from app.database.base import Base
from app.database.connection import engine
from app.models import Aeroporto
from app.api.aeroportos import router as aeroportos_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gerenciamento de Tráfego Aéreo Simulado",
    description="API inicial do projeto acadêmico de engenharia de software.",
    version="0.1.0"
)

app.include_router(aeroportos_router)


@app.get("/")
def read_root():
    return {"message": "API do sistema de tráfego aéreo simulada online."}

@app.get("/health")
def health_check():
    return {"status": "ok"}