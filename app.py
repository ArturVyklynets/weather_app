from flask import Flask, render_template, request, jsonify, redirect, url_for
from weather_api import get_weather, WeatherTime
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
# /weather?city=ivano-frankivsk&country=ukraine&time=forecast
@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")
    country = request.args.get("country")
    api = request.args.get("api")
    api = api.lower() if api else "openweather"
    time = request.args.get("time")
    time = WeatherTime.CURRENT if not time else WeatherTime(time)
    
    weather_data = get_weather(city, country, api, time)
    
    forecast_data = [
        {"date": "Понеділок", "time": "10:05", "icon": "sunny.png", "temp_min": 16, "temp_max": 26, "sunrise": "07:16", "sunset": "17:03", "pressure": "743", "humidity": "73%", "wind": "7.3", "precipitation": "10%"},
        {"date": "Вівторок", "time": "10:05", "icon": "sunny.png", "temp_min": 16, "temp_max": 26, "sunrise": "07:16", "sunset": "17:03", "pressure": "743", "humidity": "73%", "wind": "7.3", "precipitation": "10%"},
        {"date": "Середа", "time": "10:05", "icon": "cloudy.png", "temp_min": 18, "temp_max": 28, "sunrise": "07:16", "sunset": "17:03", "pressure": "743", "humidity": "73%", "wind": "7.3", "precipitation": "10%"},
        {"date": "Четвер", "time": "10:05", "icon": "rainy.png", "temp_min": 14, "temp_max": 22, "sunrise": "07:16", "sunset": "17:03", "pressure": "743", "humidity": "73%", "wind": "7.3", "precipitation": "10%"},
        {"date": "П'ятниця", "time": "10:05", "icon": "cloudy.png", "temp_min": 18, "temp_max": 28, "sunrise": "07:16", "sunset": "17:03", "pressure": "743", "humidity": "73%", "wind": "7.3", "precipitation": "10%"},
        {"date": "Субота", "time": "10:05", "icon": "rainy.png", "temp_min": 14, "temp_max": 22, "sunrise": "07:16", "sunset": "17:03", "pressure": "743", "humidity": "73%", "wind": "7.3", "precipitation": "10%"},
        {"date": "Неділя", "time": "10:05", "icon": "sunny.png", "temp_min": 16, "temp_max": 26, "sunrise": "07:16", "sunset": "17:03", "pressure": "743", "humidity": "73%", "wind": "7.3", "precipitation": "10%"},
    ]
    
    weather_info = {
        "region": "",
        "forecast": forecast_data 
    }
    if api == "openweather":
        if time == WeatherTime.CURRENT:
            weather_info.update({
                "city": weather_data["name"],
                "country": weather_data["sys"]["country"],
            })
        elif time == WeatherTime.FORECAST:
            weather_info.update({
                "city": weather_data["city"]["name"],
                "country": weather_data["city"]["country"],
            })
    elif api == "weatherapi":
        weather_info.update({
            "city": weather_data["location"]["name"],
            "country": weather_data["location"]["country"],
            "region": weather_data["location"]["region"]
        })

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

@app.errorhandler(500)
def internal_server_error(error):
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)