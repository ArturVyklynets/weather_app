from flask import Flask, render_template, request, jsonify
from weather_api import get_weather  

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)