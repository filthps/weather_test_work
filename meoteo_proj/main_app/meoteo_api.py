import openmeteo_requests
import requests_cache
from retry_requests import retry
from openmeteo_sdk.Variable import Variable


def get_weather(latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    om = openmeteo_requests.Client(session=retry_session)
    params = {
        "latitude": 52.54,
        "longitude": 13.41,
        "current": ["temperature_2m"]
    }
    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    print(dir(response.Current()))


if __name__ == "__main__":
    get_weather(0, 0)

