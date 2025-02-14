document.addEventListener("DOMContentLoaded", function () {
  const forecastContainer = document.getElementById("weather-scroll");
  const weatherDataElement = document.getElementById("weather-data");
  const imageBase = document.querySelector('script[src*="main.js"]').getAttribute("src")
  .replace("scripts/main.js", "images/");
  const forecastData = JSON.parse(weatherDataElement.textContent);
  const dayNames = ["Неділя", "Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота"];

  function getDailyForecast(data) {
    const daily = {};
    data.forEach(item => {
      const date = item.time.slice(0, 10);
      if (!daily[date]) {
        daily[date] = {
          temp_min: item.temp_min,
          temp_max: item.temp_max,
          weather: item.weather,
          description: item.description
        };
      }
      daily[date].temp_min = Math.min(daily[date].temp_min, item.temp_min);
      daily[date].temp_max = Math.max(daily[date].temp_max, item.temp_max);
    });
    return Object.keys(daily).map(date => ({
      date: date,
      temp_min: daily[date].temp_min,
      temp_max: daily[date].temp_max,
      weather: daily[date].weather,
      description: daily[date].description
    }));
  }

  const dailyForecast = getDailyForecast(forecastData);

  dailyForecast.forEach(day => {
    const d = new Date(day.date);
    const dd = String(d.getDate()).padStart(2, '0');
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const formattedDate = `${dd}.${mm}`;
    const dayOfWeek = dayNames[d.getDay()];

    const weatherImage = `${imageBase}${day.weather}.png`;
    const imageExists = checkImageExists(weatherImage) ? weatherImage : `${imageBase}default.png`;

    forecastContainer.innerHTML += `
      <div class="frame weather-card" data-city="${forecastData[0].city}>
        <p class="date">${formattedDate}</p>
        <p class="time">${dayOfWeek}</p>
        <img src="${imageExists}" alt="${day.weather}">
        <div class="range">
          <div class="range-title">
            <p>мін</p>
            <p>${Math.round(day.temp_min)} °C</p>
          </div>
          <div class="range-title">
            <p>макс</p>
            <p>${Math.round(day.temp_max)} °C</p>
          </div>
        </div>
      </div>
    `;
  });

  function checkImageExists(imagePath) {
    const xhr = new XMLHttpRequest();
    xhr.open('HEAD', imagePath, false);
    xhr.send();
    return xhr.status === 200;
  }
});


