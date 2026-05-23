<<<<<<< HEAD
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel

app = FastAPI(
    title="GeoPoints API",
    version="2.0"
)
=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3

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

<<<<<<< HEAD

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

=======
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}


# 🔍 OBTENER PUNTOS (CON FILTRO)
@app.get("/puntos")
def get_puntos(categoria: str = None):
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
    conn = get_connection()
    cur = conn.cursor()

    if categoria:
        cur.execute("""
<<<<<<< HEAD
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
=======
            SELECT id, nombre, descripcion, categoria,
                   ST_Y(geom::geometry), ST_X(geom::geometry)
            FROM puntos
            WHERE categoria = %s
        """, (categoria,))
    else:
        cur.execute("""
            SELECT id, nombre, descripcion, categoria,
                   ST_Y(geom::geometry), ST_X(geom::geometry)
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
            FROM puntos
        """)

    rows = cur.fetchall()
<<<<<<< HEAD

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

=======
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
            } for r in rows
        ]
    }


# ➕ CREAR PUNTO
@app.post("/puntos")
def crear_punto(punto: dict):
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
<<<<<<< HEAD
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

=======
        INSERT INTO puntos (nombre, descripcion, categoria, geom)
        VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s),4326))
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


# ✏️ ACTUALIZAR
@app.put("/puntos/{id}")
def actualizar_punto(id: int, punto: dict):
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE puntos
<<<<<<< HEAD
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
=======
        SET nombre=%s, descripcion=%s, categoria=%s,
            geom = ST_SetSRID(ST_MakePoint(%s, %s),4326)
        WHERE id=%s
    """, (
        punto["nombre"],
        punto["descripcion"],
        punto["categoria"],
        punto["lng"],
        punto["lat"],
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
        id
    ))

    conn.commit()
<<<<<<< HEAD

    cur.close()
    conn.close()

    return {"mensaje": "Punto actualizado correctamente"}


# ELIMINAR
@app.delete("/puntos/{id}")
def eliminar_punto(id: int):

=======
    cur.close()
    conn.close()

    return {"mensaje": "Actualizado"}


# ❌ ELIMINAR
@app.delete("/puntos/{id}")
def eliminar_punto(id: int):
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM puntos WHERE id=%s", (id,))
<<<<<<< HEAD

=======
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
    conn.commit()

    cur.close()
    conn.close()

<<<<<<< HEAD
    return {"mensaje": "Punto eliminado"}
=======
    return {"mensaje": "Eliminado"}
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3
