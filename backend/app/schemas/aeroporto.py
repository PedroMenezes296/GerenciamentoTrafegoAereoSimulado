from pydantic import BaseModel


class AeroportoResponse(BaseModel):
    id: int
    external_id: int
    identificador: str
    tipo: str
    nome: str
    latitude: float
    longitude: float
    elevacao_ft: int | None = None
    pais: str | None = None
    regiao: str | None = None
    municipio: str | None = None
    codigo_gps: str | None = None
    codigo_iata: str | None = None

    class Config:
        from_attributes = True