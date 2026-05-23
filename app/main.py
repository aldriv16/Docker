from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel

app = FastAPI(
    title="GeoPoints API",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": "geo_db",
    "database": "geopoints",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}


class Punto(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    lat: float
    lng: float


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.get("/")
def root():
    return {
        "message": "GeoPoints API funcionando 🚀"
    }


# OBTENER TODOS LOS PUNTOS
@app.get("/puntos")
def get_puntos(categoria: str = None):

    conn = get_connection()
    cur = conn.cursor()

    if categoria:
        cur.execute("""
            SELECT id,nombre,descripcion,categoria,
            ST_Y(geom::geometry),
            ST_X(geom::geometry)
            FROM puntos
            WHERE categoria=%s
        """, (categoria,))
    else:
        cur.execute("""
            SELECT id,nombre,descripcion,categoria,
            ST_Y(geom::geometry),
            ST_X(geom::geometry)
            FROM puntos
        """)

    rows = cur.fetchall()

    puntos = []

    for r in rows:
        puntos.append({
            "id": r[0],
            "nombre": r[1],
            "descripcion": r[2],
            "categoria": r[3],
            "lat": r[4],
            "lng": r[5]
        })

    cur.close()
    conn.close()

    return {"puntos": puntos}


# CREAR PUNTO
@app.post("/puntos")
def crear_punto(punto: Punto):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO puntos
        (nombre, descripcion, categoria, geom)
        VALUES (
            %s,
            %s,
            %s,
            ST_SetSRID(ST_MakePoint(%s,%s),4326)
        )
    """, (
        punto.nombre,
        punto.descripcion,
        punto.categoria,
        punto.lng,
        punto.lat
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {"mensaje": "Punto agregado correctamente"}


# ACTUALIZAR
@app.put("/puntos/{id}")
def actualizar_punto(id: int, punto: Punto):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE puntos
        SET nombre=%s,
            descripcion=%s,
            categoria=%s,
            geom=ST_SetSRID(ST_MakePoint(%s,%s),4326)
        WHERE id=%s
    """, (
        punto.nombre,
        punto.descripcion,
        punto.categoria,
        punto.lng,
        punto.lat,
        id
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {"mensaje": "Punto actualizado correctamente"}


# ELIMINAR
@app.delete("/puntos/{id}")
def eliminar_punto(id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM puntos WHERE id=%s", (id,))

    conn.commit()

    cur.close()
    conn.close()

    return {"mensaje": "Punto eliminado"}
