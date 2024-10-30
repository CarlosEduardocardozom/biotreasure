function initMap() {
    var map = L.map('map', {
        zoomControl: false
    }).setView([-14.2350, -51.9253], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.control.zoom({
        position: 'topright'
    }).addTo(map);

    var endCoords = [-21.487295776957183, -56.40119638332914]; // Buraco das Araras
    var endMarker = L.marker(endCoords).addTo(map).bindPopup('Seu Destino').openPopup();

    var startMarker = L.marker([-14.2350, -51.9253]).addTo(map).bindPopup('Sua Localização');

    // Atualiza o tempo de viagem ao selecionar o modo de transporte
    document.getElementById('transport-mode').addEventListener('change', function () {
        calculateRoute(startMarker.getLatLng(), endCoords, this.value);
    });

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    function showPosition(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;

        map.setView([lat, lon], 13);
        startMarker.setLatLng([lat, lon]);
        startMarker.bindPopup('Sua Localização').openPopup();

        // Calcule a rota inicialmente com o modo de transporte padrão (carro)
        calculateRoute([lat, lon], endCoords, document.getElementById('transport-mode').value);
    }

    function showError(error) {
        switch (error.code) {
            case error.PERMISSION_DENIED:
                alert("Usuário negou a solicitação de geolocalização.");
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Informação de localização não disponível.");
                break;
            case error.TIMEOUT:
                alert("A solicitação de geolocalização expirou.");
                break;
            case error.UNKNOWN_ERROR:
                alert("Erro desconhecido.");
                break;
        }
    }

    function calculateRoute(startCoords, endCoords, mode) {
        var apiKey = '5b3ce3597851110001cf6248c82ba0f2fc594b2496dc7a5b70919973';
        var directionsUrl = `https://api.openrouteservice.org/v2/directions/${mode}?api_key=${apiKey}&start=${startCoords[1]},${startCoords[0]}&end=${endCoords[1]},${endCoords[0]}`;

        fetch(directionsUrl)
            .then(response => response.json())
            .then(data => {
                console.log('Dados recebidos da API:', data);

                if (!data.features || data.features.length === 0) {
                    console.error('Nenhuma rota encontrada.');
                    return;
                }

                var routeCoordinates = data.features[0].geometry.coordinates;
                var latlngs = routeCoordinates.map(coord => [coord[1], coord[0]]);

                var routeLine = L.polyline(latlngs, { color: 'green', weight: 5 }).addTo(map);
                map.fitBounds(routeLine.getBounds());

                // Exibe o tempo estimado
                var duration = data.features[0].properties.segments[0].duration; // tempo em segundos
                var minutes = Math.floor(duration / 60);
                var seconds = duration % 60;
                document.getElementById('travel-time').innerText = `Tempo estimado: ${minutes} min ${seconds} seg`;
            })
            .catch(error => {
                console.error('Erro ao calcular a rota:', error);
            });
    }

    getLocation();
}

// Inicializa o mapa
initMap();
