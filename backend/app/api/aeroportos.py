from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.aeroporto import Aeroporto
from app.schemas.aeroporto import AeroportoResponse

router = APIRouter(prefix="/aeroportos", tags=["Aeroportos"])


@router.get("/", response_model=list[AeroportoResponse])
def listar_aeroportos(db: Session = Depends(get_db)):
    return db.query(Aeroporto).limit(100).all()


@router.get("/{aeroporto_id}", response_model=AeroportoResponse)
def buscar_aeroporto(aeroporto_id: int, db: Session = Depends(get_db)):
    aeroporto = db.query(Aeroporto).filter(Aeroporto.id == aeroporto_id).first()

    if not aeroporto:
        raise HTTPException(status_code=404, detail="Aeroporto não encontrado")

    return aeroporto