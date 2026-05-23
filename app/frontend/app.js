const map = L.map('map').setView([14.6349, -90.5069], 13);

L.tileLayer(
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{
    attribution:'OpenStreetMap'
}
).addTo(map);

let markers = [];

const icons = {

    cultural: L.icon({
        iconUrl:
        'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        iconSize:[32,32]
    }),

    salud: L.icon({
        iconUrl:
        'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
        iconSize:[32,32]
    }),

    servicio: L.icon({
        iconUrl:
        'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
        iconSize:[32,32]
    }),

    gastronomico: L.icon({
        iconUrl:
        'https://maps.google.com/mapfiles/ms/icons/orange-dot.png',
        iconSize:[32,32]
    })
};

map.on('click', function(e){

    document.getElementById('lat').value =
    e.latlng.lat;

    document.getElementById('lng').value =
    e.latlng.lng;
});

async function cargarPuntos(){

    markers.forEach(m => map.removeLayer(m));
    markers=[];

    try{

        const response =
        await fetch('/api/puntos');

        const data =
        await response.json();

        document.getElementById('totalPuntos')
        .innerText = data.puntos.length;

        data.puntos.forEach(p => {

            const marker = L.marker(
                [p.lat,p.lng],
                {
                    icon: icons[p.categoria]
                }
            )
            .addTo(map)
            .bindPopup(`
                <h3>${p.nombre}</h3>
                <p>${p.descripcion}</p>
                <b>${p.categoria}</b>
            `);

            markers.push(marker);
        });

    }catch(error){

        console.error(error);

        alert("Error cargando puntos");
    }
}

async function guardarPunto(){

    const nombre =
    document.getElementById('nombre').value;

    const descripcion =
    document.getElementById('descripcion').value;

    const categoria =
    document.getElementById('categoria').value;

    const lat =
    document.getElementById('lat').value;

    const lng =
    document.getElementById('lng').value;

    if(!nombre || !lat || !lng){

        alert("Completa todos los campos");
        return;
    }

    try{

        await fetch('/api/puntos',{

            method:'POST',

            headers:{
                'Content-Type':'application/json'
            },

            body:JSON.stringify({
                nombre,
                descripcion,
                categoria,
                lat,
                lng
            })
        });

        cargarPuntos();

        alert("Punto agregado");

    }catch(error){

        console.error(error);

        alert("Error guardando");
    }
}

document
.getElementById('themeBtn')
.addEventListener('click',()=>{

    document.body.classList.toggle('dark');
});

navigator.geolocation.getCurrentPosition(position=>{

    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    L.marker([lat,lng])
    .addTo(map)
    .bindPopup("📍 Tu ubicación")
    .openPopup();

    map.setView([lat,lng],13);

});

document
.getElementById('search')
.addEventListener('input', async function(){

    const texto =
    this.value.toLowerCase();

    const response =
    await fetch('/api/puntos');

    const data =
    await response.json();

    markers.forEach(m => map.removeLayer(m));
    markers=[];

    data.puntos
    .filter(p =>
        p.nombre.toLowerCase().includes(texto)
    )
    .forEach(p => {

        const marker = L.marker(
            [p.lat,p.lng],
            {
                icon: icons[p.categoria]
            }
        )
        .addTo(map)
        .bindPopup(`
            <h3>${p.nombre}</h3>
            <p>${p.descripcion}</p>
        `);

        markers.push(marker);
    });

});

cargarPuntos();
