document.addEventListener("DOMContentLoaded", function () {
  const forecastContainer = document.getElementById("weather-scroll");
  const weatherDataElement = document.getElementById("weather-data");
  const imageBase = document.querySelector('script[src*="main.js"]').getAttribute("src")
    .replace("scripts/main.js", "images/");
  const forecastData = JSON.parse(weatherDataElement.textContent);
  const dataForHourly = forecastData;


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
      <div class="frame weather-card" data-city="${forecastData[0].city}" data-date="${day.date}">  
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

  const blockOfCards = document.querySelector('.weather-scroll');
  blockOfCards.addEventListener('click', (event) => {
    const link = event.target.closest('.frame');
    const only1Day = [];
    const rawDate = link.querySelector('.date').textContent;
    const [day, month] = rawDate.split('.');
    const year = new Date().getFullYear();

    const dateObj = new Date(Date.UTC(year, month - 1, day));
    const isoDateOnly = dateObj.toISOString().split('T')[0];
    const whatINeed = dataForHourly.filter((element) => element.time.substring(0, 10) === isoDateOnly);
    console.log(whatINeed);

    if (!link) {
      return false;
    }

    renderDayForecast(whatINeed, "container");
  });

});


const DAY_PARTS = [
  { name: "НІЧ", hours: [0, 3] },
  { name: "РАНОК", hours: [6, 9] },
  { name: "ДЕНЬ", hours: [12, 15] },
  { name: "ВЕЧІР", hours: [18, 21] },
];

function formatHHMM(dateStr) {
  const d = new Date(dateStr);
  return `${String(d.getUTCHours()).padStart(2, "0")}:${String(d.getUTCMinutes()).padStart(2, "0")}`;
}

function findForecastByHour(data, hours) {
  return hours.map(h => data.find(f => new Date(f.time).getUTCHours() === h) || null);
}

function processDayForecast(dayData) {
  const dateObj = new Date(dayData[0].time);
  const weekday = ["Неділя", "Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця", "Субота"][dateObj.getUTCDay()];
  const dateDM = `${String(dateObj.getUTCDate()).padStart(2, "0")}.${String(dateObj.getUTCMonth() + 1).padStart(2, "0")}`;

  const sunriseStr = dayData[0].sunrise ? formatHHMM(dayData[0].sunrise) : "";
  const sunsetStr = dayData[0].sunset ? formatHHMM(dayData[0].sunset) : "";

  const parts = DAY_PARTS.reduce((acc, part) => {
    const [f1, f2] = findForecastByHour(dayData, part.hours);

    const partData = [
      {
        times: [`${extractTime(f1.time)}`],
        temperature: f1.temperature,
        pressure: f1.pressure,
        humidity: f1.humidity,
        wind: f1.wind,
        precip: convertToPercentage(f1.precipitation?.rain) + convertToPercentage(f1.precipitation?.snow)
      },
      {
        times: [`${extractTime(f2.time)}`],
        temperature: f2.temperature,
        pressure: f2.pressure,
        humidity: f2.humidity,
        wind: f2.wind,
        precip: convertToPercentage(f2.precipitation?.rain) + convertToPercentage(f2.precipitation?.snow)
      }
    ];

    acc[part.name] = partData;
    return acc;
  }, {});

  return { dateDM, weekday, sunriseStr, sunsetStr, parts };
}



function renderDayForecast(dayData, containerId) {
  const day = processDayForecast(dayData);
  console.log(day);

  const html = `
      <article class="weather-day">
      <div class="weather-container">
        <div class="day-info">
          <h2>${day.weekday}</h2>
          <h1>${day.dateDM}</h1>
          <div class="sun-info">
            <p><span class="label">Схід</span> <span class="time">${day.sunriseStr}</span></p>
            <p><span class="label">Захід</span> <span class="time">${day.sunsetStr}</span></p>
          </div>
        </div>

        <div class="forecast weather-table">
              <div class="labels">
                  <p>Температура</p>
                  <p>Тиск</p>
                  <p>Вологість</p>
                  <p>Вітер</p>
                  <p>Ймовірність опадів</p>
              </div>
              ${Object.keys(day.parts).map(partName => {
    const icon = partName.toLowerCase();
    return `
                <div class="forecast-card">
                  <h3>${partName}</h3>
                  <img src="../static/images/${icon}.png" alt="${icon}" class="forecast-icon" />
                  <div class="forecast-columns">
                    ${day.parts[partName].map(forecast => `
                      <div class="forecast-column values">
                        <p>${forecast.times[0]}</p>
                      <p>${forecast.temperature}°C</p>
                        <p>${forecast.pressure}</p>
                        <p>${forecast.humidity}</p>
                        <p>${forecast.wind}</p>
                        <p>${forecast.precip}%</p>
                      </div>
                    `).join('')}
                  </div>
                </div>
              `}).join('')}
        </div>
        </div>
      </article>`;

  document.getElementById(containerId).innerHTML = html;
}

function convertToPercentage(value) {
  return value * 100;
}

function extractTime(dateString) {
  const dateObj = new Date(dateString);
  return dateObj.toISOString().slice(11, 16);
}