from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "6e1af1e6c02bb73d5bab72a8285d922c"  # OpenWeatherMap API ключ
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
