from flask import Flask, render_template, request, jsonify, redirect, url_for
from weather_api import get_weather, WeatherTime, normalize_openweathermap, normalize_weatherapi
from capitals import load_capitals
from country_api import get_country_from_city
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)

capitals = load_capitals()
executor = ThreadPoolExecutor(max_workers=10)

@app.route("/")
def index():
    return render_template("index.html")

# api testing, currently simply outputs json data
# /weather?city=kyiv&country=ukraine?api=weatherapi
# /weather?city=ivano-frankivsk&country=ukraine&time=forecast
@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")
    country = get_country_from_city(city)
    api = request.args.get("api", "openweather").lower()
    time = request.args.get("time", "forecast")

    try:
        time = WeatherTime(time)
    except ValueError:
        time = WeatherTime.CURRENT

    weather_data = get_weather(city, country, api, time)

    if not weather_data:
        return redirect(url_for('index'))

    if api == "openweather":
        weather_data = normalize_openweathermap(weather_data, time)
    elif api == "weatherapi":
        weather_data = normalize_weatherapi(weather_data, time)

    weather_info = {
        "city": weather_data["city"],
        "country": weather_data["country"],
        "forecast": weather_data.get("forecast", [])
    }
    
    return render_template("weather.html", weather=weather_info)


# Обробка погоди для виведення на мапу
@app.route("/weather_all")
def weather_all():
    weather_data = []
    def fetch_weather_for_capital(capital):
        weather = get_weather(capital["city"], capital["country"], "openweather")
        if not weather or weather.get("cod") == "404":
            print(f" Пропускаємо {capital['city']} (не знайдено в OpenWeather)")
            return None

        return {
            "city": capital["city"],
            "country": capital["country"],
            "lat": capital["lat"],
            "lon": capital["lon"],
            "temperature": weather["main"]["temp"],
            "description": weather["weather"][0]["description"]
        }

    future_results = [executor.submit(fetch_weather_for_capital, capital) for capital in capitals]

    for future in future_results:
        result = future.result()
        if result: 
            weather_data.append(result)

    print(f"Отримано {len(weather_data)} міст з погодою.")
    return jsonify(weather_data)

# @app.errorhandler(500)
# def internal_server_error(error):
#     return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)