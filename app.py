from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY_OPENWEATHER = "6e1af1e6c02bb73d5bab72a8285d922c"  # OpenWeatherMap API ключ
API_KEY_WEATHERSTACK = "3e45c55430d64740bef182024250802"  # API ключ для Weatherstack

BASE_URL_OPENWEATHER = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_WEATHERSTACK = "http://api.weatherstack.com/current"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data_openweathermap = None
    weather_data_weatherstack = None

    if request.method == "POST":
        city = request.form.get("city")
        print(f"Отримане місто: {city}")  # Виведе місто в термінал

        if city:
            # Запит до OpenWeatherMap
            # params_openweathermap = {"q": city, "appid": API_KEY_OPENWEATHER, "units": "metric", "lang": "uk"}
            # response_openweathermap = requests.get(BASE_URL_OPENWEATHER, params=params_openweathermap)
            # print(f"Статус-код OpenWeatherMap: {response_openweathermap.status_code}")  # Виведе статус-запиту

            # if response_openweathermap.status_code == 200:
            #   weather_data_openweathermap = response_openweathermap.json()
            #   print(f"Дані OpenWeatherMap: {weather_data_openweathermap}")

            # Запит до Weatherstack
            params_weatherstack = {"access_key": API_KEY_WEATHERSTACK, "q": city, "lang": "uk"}
            response_weatherstack = requests.get(BASE_URL_WEATHERSTACK, params=params_weatherstack)
            print(f"Статус-код Weatherstack: {response_weatherstack.status_code}")  # Виведе статус-запиту

            if response_weatherstack.status_code == 200:
              weather_data_weatherstack = response_weatherstack.json()
              print(f"Дані Weatherstack: {weather_data_weatherstack}")

    return render_template("index.html", 
                           weather_openweathermap=weather_data_openweathermap, 
                           weather_weatherstack=weather_data_weatherstack)


if __name__ == "__main__":
    app.run(debug=True)
