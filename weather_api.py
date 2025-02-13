import requests
import enum
from datetime import datetime, timezone
import pytz
import pycountry

def unix_to_iso(unix):
    return datetime.fromtimestamp(unix, timezone.utc).isoformat()

def weatherapi_to_iso(tz_id, time):
    tz = pytz.timezone(tz_id)
    time = datetime.strptime(time, "%Y-%m-%d %I:%M %p")
    time = tz.localize(time)
    return time.astimezone(pytz.utc).isoformat()

def country_code_to_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

class WeatherTime(enum.Enum):
    CURRENT = "current"
    FORECAST = "forecast"

OPENWEATHER_API_KEY = "6e1af1e6c02bb73d5bab72a8285d922c"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

WEATHERAPI_KEY = "3e45c55430d64740bef182024250802"
WEATHERAPI_URL = "http://api.weatherapi.com/v1/current.json"
WEATHERAPI_FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json"

class Weather(enum.Enum):
    THUNDERSTORM = "thunderstorm"
    DRIZZLE = "drizzle"
    RAIN = "rain"
    SNOW = "snow"
    MIST = "mist"
    SMOKE = "smoke"
    HAZE = "haze"
    DUST = "dust"
    FOG = "fog"
    SAND = "sand"
    ASH = "ash"
    SQUALL = "squall"
    TORNADO = "tornado"
    CLEAR = "clear"
    CLOUDS = "clouds"

openweather_status_codes = {
    200: Weather.THUNDERSTORM,
    201: Weather.THUNDERSTORM,
    202: Weather.THUNDERSTORM,
    210: Weather.THUNDERSTORM,
    211: Weather.THUNDERSTORM,
    212: Weather.THUNDERSTORM,
    221: Weather.THUNDERSTORM,
    230: Weather.THUNDERSTORM,
    231: Weather.THUNDERSTORM,
    232: Weather.THUNDERSTORM,
    300: Weather.DRIZZLE,
    301: Weather.DRIZZLE,
    302: Weather.DRIZZLE,
    310: Weather.DRIZZLE,
    311: Weather.DRIZZLE,
    312: Weather.DRIZZLE,
    313: Weather.DRIZZLE,
    314: Weather.DRIZZLE,
    321: Weather.DRIZZLE,
    500: Weather.RAIN,
    501: Weather.RAIN,
    502: Weather.RAIN,
    503: Weather.RAIN,
    504: Weather.RAIN,
    511: Weather.RAIN,
    520: Weather.RAIN,
    521: Weather.RAIN,
    522: Weather.RAIN,
    531: Weather.RAIN,
    600: Weather.SNOW,
    601: Weather.SNOW,
    602: Weather.SNOW,
    611: Weather.SNOW,
    612: Weather.SNOW,
    613: Weather.SNOW,
    615: Weather.SNOW,
    616: Weather.SNOW,
    620: Weather.SNOW,
    621: Weather.SNOW,
    622: Weather.SNOW,
    701: Weather.MIST,
    711: Weather.SMOKE,
    721: Weather.HAZE,
    731: Weather.DUST,
    741: Weather.FOG,
    751: Weather.SAND,
    761: Weather.DUST,
    762: Weather.ASH,
    771: Weather.SQUALL,
    781: Weather.TORNADO,
    800: Weather.CLEAR,
    801: Weather.CLOUDS,
    802: Weather.CLOUDS,
    803: Weather.CLOUDS,
    804: Weather.CLOUDS
}

weartherapi_status_codes = {
    1000: Weather.CLEAR,
    1003: Weather.CLOUDS,
    1006: Weather.CLOUDS,
    1009: Weather.CLOUDS,
    1030: Weather.MIST,
    1063: Weather.RAIN,
    1066: Weather.SNOW,
    1069: Weather.SNOW,
    1072: Weather.SNOW,
    1087: Weather.THUNDERSTORM,
    1114: Weather.SNOW,
    1117: Weather.SNOW,
    1135: Weather.FOG,
    1147: Weather.FOG,
    1150: Weather.DRIZZLE,
    1153: Weather.DRIZZLE,
    1168: Weather.DRIZZLE,
    1171: Weather.DRIZZLE,
    1180: Weather.RAIN,
    1183: Weather.RAIN,
    1186: Weather.RAIN,
    1189: Weather.RAIN,
    1192: Weather.RAIN,
    1195: Weather.RAIN,
    1198: Weather.RAIN,
    1201: Weather.RAIN,
    1204: Weather.RAIN,
    1207: Weather.RAIN,
    1210: Weather.SNOW,
    1213: Weather.SNOW,
    1216: Weather.SNOW,
    1219: Weather.SNOW,
    1222: Weather.SNOW,
    1225: Weather.SNOW,
    1237: Weather.SNOW,
    1240: Weather.RAIN,
    1243: Weather.RAIN,
    1246: Weather.RAIN,
    1249: Weather.RAIN,
    1252: Weather.RAIN,
    1255: Weather.SNOW,
    1258: Weather.SNOW,
    1261: Weather.SNOW,
    1264: Weather.SNOW,
    1273: Weather.THUNDERSTORM,
    1276: Weather.THUNDERSTORM,
    1279: Weather.THUNDERSTORM,
    1282: Weather.THUNDERSTORM
}

def normalize_openweathermap(data, time=WeatherTime.CURRENT):
    if time == WeatherTime.CURRENT:
        return {
            "city": data["name"],
            "country": country_code_to_name(data["sys"]["country"]),
            "temperature": data["main"]["temp"],
            "weather": openweather_status_codes.get(data["weather"][0]["id"], None).value if openweather_status_codes.get(data["weather"][0]["id"], None) else None,
            "description": data["weather"][0]["description"]
        }
    elif time == WeatherTime.FORECAST:
        return {
            "city": data["city"]["name"],
            "country": country_code_to_name(data["city"]["country"]),
            "forecast": [
                {
                    "temperature": forecast["main"]["temp"],
                    "temp_min": forecast["main"]["temp_min"],
                    "temp_max": forecast["main"]["temp_max"],
                    "sunrise": unix_to_iso(data["city"]["sunrise"]),
                    "sunset": unix_to_iso(data["city"]["sunset"]),
                    "pressure": forecast["main"]["pressure"],
                    "humidity": forecast["main"]["humidity"],
                    "wind": forecast["wind"]["speed"],
                    "precipitation": {
                        "rain": forecast.get("rain", {}).get("3h", 0),
                        "snow": forecast.get("snow", {}).get("3h", 0)
                    },
                    "weather": openweather_status_codes.get(forecast["weather"][0]["id"], None).value if openweather_status_codes.get(forecast["weather"][0]["id"], None) else None,
                    "description": forecast["weather"][0]["description"],
                    "time": unix_to_iso(forecast["dt"])
                }
                for forecast in data["list"]
            ]
        }

def normalize_weatherapi(data, time=WeatherTime.CURRENT):
    if time == WeatherTime.CURRENT:
        return {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "weather": weartherapi_status_codes.get(data["current"]["condition"]["code"], None).value if weartherapi_status_codes.get(data["current"]["condition"]["code"], None) else None,
            "description": data["current"]["condition"]["text"]
        }
    elif time == WeatherTime.FORECAST:
        tz_id = data["location"]["tz_id"]
        output = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "region": data["location"]["region"],
            "forecast": []
        }
        for forecast in data["forecast"]["forecastday"]:
            for hour in forecast["hour"]:
                output["forecast"].append({
                    "temperature": hour["temp_c"],
                    "temp_min": forecast["day"]["mintemp_c"],
                    "temp_max": forecast["day"]["maxtemp_c"],
                    "sunrise": weatherapi_to_iso(tz_id, forecast["date"] + " " + forecast["astro"]["sunrise"]),
                    "sunset": weatherapi_to_iso(tz_id, forecast["date"] + " " + forecast["astro"]["sunset"]),
                    "pressure": hour["pressure_mb"],
                    "humidity": hour["humidity"],
                    "wind": hour["wind_kph"],
                    "precipitation": {
                        "rain": hour["precip_mm"],
                        "snow": hour["snow_cm"] * 10
                    },
                    "weather": weartherapi_status_codes.get(hour["condition"]["code"], None).value if weartherapi_status_codes.get(hour["condition"]["code"], None) else None,
                    "description": hour["condition"]["text"],
                    "time": unix_to_iso(hour["time_epoch"])
                })
        return output
    

def get_weather(city, country, api="openweather", time=WeatherTime.CURRENT):
    if api == "openweather":
        params = {
            "q": f"{city},{country}",
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "uk"
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
            "lang": "uk"
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