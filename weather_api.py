import requests
import enum

class WeatherTime(enum.Enum):
    CURRENT = "current"
    FORECAST = "forecast"

OPENWEATHER_API_KEY = "6e1af1e6c02bb73d5bab72a8285d922c"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

WEATHERAPI_KEY = "3e45c55430d64740bef182024250802"
WEATHERAPI_URL = "http://api.weatherapi.com/v1/current.json"
WEATHERAPI_FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json"

def get_weather(city, country, api="openweather", time=WeatherTime.CURRENT):
    if api == "openweather":
        params = {
            "q": f"{city},{country}",
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "ua"
        }
        if time == WeatherTime.CURRENT:
            response = requests.get(OPENWEATHER_URL, params=params)
            data = response.json()
            return data
        elif time == WeatherTime.FORECAST:
            response = requests.get(OPENWEATHER_FORECAST_URL, params=params)
            data = response.json()
            return data
    elif api == "weatherapi":
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{city},{country}",
            "lang": "ua"
        }
        if time == WeatherTime.CURRENT:
            response = requests.get(WEATHERAPI_URL, params=params)
            data = response.json()
            return data
        elif time == WeatherTime.FORECAST:
            params["days"] = 3
            response = requests.get(WEATHERAPI_FORECAST_URL, params=params)
            data = response.json()
            return data
    else:
        return None