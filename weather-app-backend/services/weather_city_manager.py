import requests
import os

class WeatherCityManager:
    _instance = None
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_instance():

        if WeatherCityManager._instance is None:
            WeatherCityManager()
        return WeatherCityManager._instance

    def __init__(self):

        if WeatherCityManager._instance is not None:
            raise Exception("Access this class using get_instance()")
        else:
            WeatherCityManager._instance = self

        self.api_key = os.getenv('API_KEY')

    def get_weather_for_city(self, city_name):

        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric" 
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            return None
