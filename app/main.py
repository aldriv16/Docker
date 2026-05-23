from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# =========================
# API ENDPOINTS
# =========================
@app.get("/puntos")
def obtener_puntos():

    query = text("""
        SELECT id, nombre, latitud, longitud
        FROM puntos_interes
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        puntos = []

        for row in result:
            puntos.append({
                "id": row.id,
                "nombre": row.nombre,
                "latitud": row.latitud,
                "longitud": row.longitud
            })

        return puntos


# =========================
# FRONTEND
# =========================
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
def home():
    return FileResponse(os.path.join(frontend_path, "index.html"))
