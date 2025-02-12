import requests

OPENWEATHER_API_KEY = "6e1af1e6c02bb73d5bab72a8285d922c"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

WEATHERAPI_KEY = "3e45c55430d64740bef182024250802"
WEATHERAPI_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(city, country, api="openweather"):
    if api == "openweather":
        params = {
            "q": f"{city},{country}",
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "ua"
        }
        response = requests.get(OPENWEATHER_URL, params=params)
        data = response.json()
        return data
    elif api == "weatherapi":
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{city},{country}",
            "lang": "ua"
        }
        response = requests.get(WEATHERAPI_URL, params=params)
        data = response.json()
        return data["current"]
    else:
        return None