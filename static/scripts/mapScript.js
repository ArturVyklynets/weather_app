var map = L.map('map', {zoomControl: false}).setView([50, 10], 5);
    
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);
var customIcon = L.icon({
  iconUrl: '/static/images/marker.png',
  iconSize: [32, 42],
  iconAnchor: [15, 42],
  popupAnchor: [0, -32] 
});

fetch("/weather_all")
    .then(response => response.json())
    .then(data => {
        data.forEach(city => {
            var marker = L.marker([city.lat, city.lon], { icon: customIcon }).addTo(map);
            marker.bindPopup(
                `<b>${city.city}, ${city.country}</b><br>` +
                `Температура: ${city.temperature}°C<br>` +
                `Погода: ${city.description}`
            );
        });
    })
    .catch(error => console.error("Помилка отримання даних:", error));