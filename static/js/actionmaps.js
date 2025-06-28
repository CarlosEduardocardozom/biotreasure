let map;
let currentLayer;
let userLocation = null;
let routeLayerGroup = null;

const icons = {
  restaurant: L.icon({
    iconUrl: '/static/media/pin-icon.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  }),
  transport: L.icon({
    iconUrl: '/static/media/transport-icon.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  }),
  default: L.icon({
    iconUrl: '/static/media/default-icon.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  })
};

window.onload = () => {
  initMap();
  initSearchAndCategories();
};

function calculateRoute(start, end) {
  const mode = document.getElementById('transport-mode').value;
  const apiKey = '5b3ce3597851110001cf6248c82ba0f2fc594b2496dc7a5b70919973';
  const url =
    `https://api.openrouteservice.org/v2/directions/${mode}?api_key=${apiKey}` +
    `&start=${start.lng},${start.lat}&end=${end[1]},${end[0]}`;

  fetch(url)
    .then(res => res.json())
    .then(data => {
      if (!data.features?.length) return;

      const coords = data.features[0].geometry.coordinates.map(c => [c[1], c[0]]);

      if (routeLayerGroup) map.removeLayer(routeLayerGroup);
      routeLayerGroup = L.layerGroup().addTo(map);

      L.polyline(coords, { color: 'green', weight: 5 }).addTo(routeLayerGroup);
      map.fitBounds(coords);

      const secs = data.features[0].properties.segments[0].duration;
      const min = Math.floor(secs / 60), sec = Math.floor(secs % 60);
      document.getElementById('travel-time').innerText = `Tempo: ${min}min ${sec}s`;
    })
    .catch(console.error);
}

function initMap() {
  map = L.map('map', { zoomControl: false }).setView([-14.2350, -51.9253], 5);

  currentLayer = L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { attribution: '© OpenStreetMap contributors' }
  ).addTo(map);

  const endCoords = [-21.487295776957183, -56.40119638332914];
  const startMarker = L.marker([-14.2350, -51.9253]).addTo(map).bindPopup('Sua Localização');
  L.marker(endCoords).addTo(map).bindPopup('Seu Destino');

  document.getElementById('transport-mode')?.addEventListener('change', () => {
    if (userLocation) {
      calculateRoute(userLocation, endCoords);
    }
  });

  navigator.geolocation.getCurrentPosition(
    pos => {
      const lat = pos.coords.latitude, lng = pos.coords.longitude;
      userLocation = { lat, lng };
      map.setView([lat, lng], 13);
      startMarker.setLatLng([lat, lng]).openPopup();
      calculateRoute(userLocation, endCoords);
    },
    err => alert('Erro na geolocalização: ' + err.message)
  );

  document.getElementById('zoom-in')?.addEventListener('click', () => map.zoomIn());
  document.getElementById('zoom-out')?.addEventListener('click', () => map.zoomOut());

  const toggleBtn = document.getElementById('toggle-map');
  const menu = document.getElementById('layer-menu');
  toggleBtn?.addEventListener('click', () => {
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
  });
  document.addEventListener('click', e => {
    if (!menu.contains(e.target) && !toggleBtn.contains(e.target)) {
      menu.style.display = 'none';
    }
  });

  document.querySelectorAll('#layer-menu .layer-option').forEach(el => {
    el.addEventListener('click', () => {
      map.removeLayer(currentLayer);
      currentLayer = L.tileLayer(el.dataset.url, { attribution: el.dataset.attrib }).addTo(map);
      menu.style.display = 'none';
    });
  });

  document.getElementById('locate-btn')?.addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition(pos => {
      const lat = pos.coords.latitude, lng = pos.coords.longitude;
      userLocation = { lat, lng };
      map.setView([lat, lng], 13);
      L.marker([lat, lng], {
        icon: L.icon({
          iconUrl: '/static/media/locate-icon.png',
          iconSize: [50, 50]
        })
      }).addTo(map).bindPopup('Você está aqui').openPopup();
    });
  });

  map.on('click', e => {
    const lat = e.latlng.lat.toFixed(6);
    const lng = e.latlng.lng.toFixed(6);
    const content = `
      <strong>Destino:</strong> ${lat}, ${lng}<br/>
      <button onclick="calculateRoute(userLocation, [${lat}, ${lng}])">
        Traçar rota até aqui
      </button>
    `;
    L.popup().setLatLng(e.latlng).setContent(content).openOn(map);
  });
}

function initSearchAndCategories() {
  async function searchPlace(q) {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}`
    );
    return res.json();
  }

  document.getElementById('search-btn')?.addEventListener('click', async () => {
    const q = document.getElementById('place-search').value;
    const results = await searchPlace(q);
    if (results.length) {
      const r = results[0];
      const lat = parseFloat(r.lat);
      const lng = parseFloat(r.lon);
      const marker = L.marker([lat, lng], { icon: icons.default }).addTo(map);
      const content = `
        <strong>${r.display_name}</strong><br/>
        <button onclick="calculateRoute(userLocation, [${lat}, ${lng}])">
          Traçar rota
        </button>
      `;
      marker.bindPopup(content).openPopup();
      map.setView([lat, lng], 14);
    }
  });

  async function searchCategory(cat) {
    const b = map.getBounds();
    const bbox = `${b.getSouth()},${b.getWest()},${b.getNorth()},${b.getEast()}`;
    const query = `[out:json];node[amenity=${cat}](${bbox});out;`;
    const res = await fetch(
      'https://overpass-api.de/api/interpreter?data=' + encodeURIComponent(query)
    );
    const data = await res.json();

    const iconType =
      cat === 'restaurant' ? 'restaurant' :
      (cat === 'bus_station' || cat === 'train_station') ? 'transport' :
      'default';

    data.elements.forEach(el => {
      const lat = el.lat, lng = el.lon;
      const popup = `
        <strong>${el.tags.name || cat}</strong><br/>
        <button onclick="calculateRoute(userLocation, [${lat}, ${lng}])">
          Traçar rota
        </button>
      `;
      L.marker([lat, lng], { icon: icons[iconType] }).addTo(map).bindPopup(popup);
    });
  }

  document.querySelectorAll('#search-categories .cat-buttons button').forEach(btn => {
    btn.addEventListener('click', () => searchCategory(btn.dataset.cat));
  });
}
