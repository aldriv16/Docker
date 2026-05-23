from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

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

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# =========================
# FRONTEND
# =========================
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def home():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# =========================
# API STATUS
# =========================
@app.get("/api")
def api_status():
    return {"message": "API funcionando correctamente 🚀"}

# =========================
# OBTENER PUNTOS
# =========================
@app.get("/api/puntos")
def get_puntos(categoria: str = None):

    conn = get_connection()
    cur = conn.cursor()

    if categoria:
        cur.execute("""
            SELECT id, nombre, descripcion, categoria,
                   ST_Y(geom::geometry),
                   ST_X(geom::geometry)
            FROM puntos
            WHERE categoria = %s
        """, (categoria,))
    else:
        cur.execute("""
            SELECT id, nombre, descripcion, categoria,
                   ST_Y(geom::geometry),
                   ST_X(geom::geometry)
            FROM puntos
        """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "puntos": [
            {
                "id": r[0],
                "nombre": r[1],
                "descripcion": r[2],
                "categoria": r[3],
                "lat": r[4],
                "lng": r[5]
            }
            for r in rows
        ]
    }

# =========================
# CREAR PUNTO
# =========================
@app.post("/api/puntos")
def crear_punto(punto: dict):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO puntos
        (nombre, descripcion, categoria, geom)
        VALUES (
            %s,
            %s,
            %s,
            ST_SetSRID(ST_MakePoint(%s, %s),4326)
        )
    """, (
        punto["nombre"],
        punto["descripcion"],
        punto["categoria"],
        punto["lng"],
        punto["lat"]
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {"mensaje": "Punto creado"}

# =========================
# ACTUALIZAR
# =========================
@app.put("/api/puntos/{id}")
def actualizar_punto(id: int, punto: dict):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE puntos
        SET
            nombre=%s,
            descripcion=%s,
            categoria=%s,
            geom=ST_SetSRID(
                ST_MakePoint(%s,%s),
                4326
            )
        WHERE id=%s
    """, (
        punto["nombre"],
        punto["descripcion"],
        punto["categoria"],
        punto["lng"],
        punto["lat"],
        id
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {"mensaje": "Punto actualizado"}

# =========================
# ELIMINAR
# =========================
@app.delete("/api/puntos/{id}")
def eliminar_punto(id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM puntos WHERE id=%s",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"mensaje": "Punto eliminado"}
