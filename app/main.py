from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import create_engine, text
import os

app = FastAPI(title="Sistema de Registro de Puntos de Interés")

# =========================
# CONEXIÓN A POSTGRESQL
# =========================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgress:JMcQorcgMrqlKycZ39nxridK0MPY3ang@dpg-d88ge7egvqtc73b34tg0-a.oregon-postgres.render.com/geopoints"
)

engine = create_engine(DATABASE_URL)

# =========================
# FRONTEND
# =========================

frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# =========================
# RUTA PRINCIPAL
# =========================

@app.get("/")
def home():
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)

# =========================
# API PUNTOS
# =========================

@app.get("/api/puntos")
def obtener_puntos():

    try:
        with engine.connect() as connection:

            resultado = connection.execute(text("""
                SELECT id, nombre, descripcion, latitud, longitud
                FROM puntos_interes
                ORDER BY id ASC
            """))

            puntos = []

            for fila in resultado:
                puntos.append({
                    "id": fila.id,
                    "nombre": fila.nombre,
                    "descripcion": fila.descripcion,
                    "latitud": float(fila.latitud),
                    "longitud": float(fila.longitud)
                })

            return JSONResponse(content=puntos)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
