from flask import Flask, render_template, request, jsonify
from weather_api import get_weather  

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("weather.html")

# api testing, currently simply outputs json data
# /weather?city=kyiv&country=ukraine?api=weatherapi
# /weather?city=ivano-frankivsk&country=ukraine
@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")
    country = request.args.get("country")
    api = request.args.get("api")
    api = api.lower() if api else "openweather"
    result = get_weather(city, country, api)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)