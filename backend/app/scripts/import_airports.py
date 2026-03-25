import csv
from pathlib import Path

from app.database.connection import SessionLocal
from app.models.aeroporto import Aeroporto


TIPOS_VALIDOS = {"small_airport", "medium_airport", "large_airport"}


def to_int(value):
    if value in (None, "", "NULL"):
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def to_float(value):
    if value in (None, "", "NULL"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def import_airports():
    db = SessionLocal()

    try:
        csv_path = Path(__file__).resolve().parents[2] / "data" / "airports.csv"

        if not csv_path.exists():
            print(f"Arquivo não encontrado: {csv_path}")
            return

        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            total_lidos = 0
            total_importados = 0
            total_ignorados = 0

            for row in reader:
                total_lidos += 1

                if row["type"] not in TIPOS_VALIDOS:
                    total_ignorados += 1
                    continue

                external_id = to_int(row["id"])
                latitude = to_float(row["latitude_deg"])
                longitude = to_float(row["longitude_deg"])

                if external_id is None or latitude is None or longitude is None:
                    total_ignorados += 1
                    continue

                ja_existe = (
                    db.query(Aeroporto)
                    .filter(Aeroporto.external_id == external_id)
                    .first()
                )

                if ja_existe:
                    total_ignorados += 1
                    continue

                aeroporto = Aeroporto(
                    external_id=external_id,
                    identificador=row["ident"],
                    tipo=row["type"],
                    nome=row["name"],
                    latitude=latitude,
                    longitude=longitude,
                    elevacao_ft=to_int(row["elevation_ft"]),
                    pais=row["iso_country"] or None,
                    regiao=row["iso_region"] or None,
                    municipio=row["municipality"] or None,
                    codigo_gps=row["gps_code"] or None,
                    codigo_iata=row["iata_code"] or None,
                )

                db.add(aeroporto)
                total_importados += 1

            db.commit()

            print("Importação concluída com sucesso.")
            print(f"Total lidos: {total_lidos}")
            print(f"Total importados: {total_importados}")
            print(f"Total ignorados: {total_ignorados}")

    except Exception as e:
        db.rollback()
        print(f"Erro durante a importação: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    import_airports()