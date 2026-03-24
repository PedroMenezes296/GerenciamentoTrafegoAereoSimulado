from sqlalchemy import Column, Integer, String, Float
from app.database.base import Base


class Aeroporto(Base):
    __tablename__ = "aeroportos"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, nullable=False, index=True)
    identificador = Column(String, nullable=False, index=True)
    tipo = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevacao_ft = Column(Integer, nullable=True)
    pais = Column(String, nullable=True)
    regiao = Column(String, nullable=True)
    municipio = Column(String, nullable=True)
    codigo_gps = Column(String, nullable=True)
    codigo_iata = Column(String, nullable=True)