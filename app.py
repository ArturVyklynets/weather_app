from flask import Flask, render_template, request, jsonify
from weather_api import get_weather  
from capitals import load_capitals
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)

capitals = load_capitals()
executor = ThreadPoolExecutor(max_workers=10)

@app.route("/")
def index():
    return render_template("index.html")

# api testing, currently simply outputs json data
# /weather?city=kyiv&country=ukraine?api=weatherapi
# /weather?city=ivano-frankivsk&country=ukraine
@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")
    country = request.args.get("country")
    api = request.args.get("api")
    api = api.lower() if api else "openweather"
    weather_data = get_weather(city, country, api)
    forecast_data = [
        {"date": "Понеділок", "time": "10:05", "icon": "sunny.png", "temp_min": 16, "temp_max": 26},
        {"date": "Вівторок", "time": "10:05", "icon": "sunny.png", "temp_min": 16, "temp_max": 26},
        {"date": "Середа", "time": "10:05", "icon": "cloudy.png", "temp_min": 18, "temp_max": 28},
        {"date": "Четвер", "time": "10:05", "icon": "rainy.png", "temp_min": 14, "temp_max": 22},
        {"date": "П'ятниця", "time": "10:05", "icon": "windy.png", "temp_min": 12, "temp_max": 20},
        {"date": "Субота", "time": "10:05", "icon": "storm.png", "temp_min": 10, "temp_max": 18},
        {"date": "Неділя", "time": "10:05", "icon": "snowy.png", "temp_min": 5, "temp_max": 10},
    ]

    weather_info = {
        "city": weather_data["name"],
        "country": weather_data["sys"]["country"],
        "region": "Львівська область",
        "forecast": forecast_data 
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

if __name__ == "__main__":
    app.run(debug=True)