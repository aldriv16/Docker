CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS puntos;

CREATE TABLE puntos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    categoria VARCHAR(50),
    geom GEOGRAPHY(Point,4326)
);

INSERT INTO puntos (nombre, descripcion, categoria, geom)
VALUES
('Parque Central', 'Centro histórico', 'cultural', ST_SetSRID(ST_MakePoint(-90.5133,14.6349),4326)),
('Gasolinera', 'Estación de servicio', 'servicio', ST_SetSRID(ST_MakePoint(-90.5200,14.6300),4326)),
('Museo Nacional', 'Museo cultural', 'cultural', ST_SetSRID(ST_MakePoint(-90.5150,14.6400),4326)),
('Restaurante', 'Comida típica', 'gastronomico', ST_SetSRID(ST_MakePoint(-90.5100,14.6350),4326)),
('Hospital', 'Centro médico', 'salud', ST_SetSRID(ST_MakePoint(-90.5170,14.6380),4326));
