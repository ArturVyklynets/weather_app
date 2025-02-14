import requests

GEOCODE_API_KEY = "3586b6eb964644a69f65ddb1b8a40633"  

def get_country_from_city(city):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={GEOCODE_API_KEY}&language=uk"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        country = data['results'][0]['components'].get('country', '')
        return country
    return None
