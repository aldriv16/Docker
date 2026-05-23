// =========================
// MAPA
// =========================
const map = L.map('map').setView([14.6349, -90.5069], 13);

// =========================
// CAPA MAPA
// =========================
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// =========================
// ICONO PERSONALIZADO
// =========================
const customIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
    iconSize: [38, 38],
    iconAnchor: [19, 38],
    popupAnchor: [0, -38]
});

// =========================
// CARGAR PUNTOS
// =========================
fetch('/puntos')
    .then(response => response.json())
    .then(data => {

        console.log("Puntos cargados:", data);

        data.forEach(punto => {

            L.marker([punto.latitud, punto.longitud], {
                icon: customIcon
            })
            .addTo(map)
            .bindPopup(`
                <b>${punto.nombre}</b><br>
                Latitud: ${punto.latitud}<br>
                Longitud: ${punto.longitud}
            `);

        });

    })
    .catch(error => {
        console.error("Error cargando puntos:", error);
    });
