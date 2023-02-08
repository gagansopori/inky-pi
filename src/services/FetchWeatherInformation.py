import json, urllib.request
from urllib.error import URLError

from src.services import base_weather_url, imperial_countries, owm_key
from src.services.WeatherModel import WeatherModel


class FetchWeatherInformation:
    def __init__(self):
        self.weather_data = WeatherModel()

    def get_weather(self, geo_coordinates) -> WeatherModel:
        """
        This method takes geographical coordinates & calls the open-weather api to determine the weather conditions for
        a given set of geo-coordinates.
        :param geo_coordinates: (latitude, longitude)
        :return: current_temperature, weather_condition, icon_id
        """
        # Build the location based url
        weather_url = f'{base_weather_url}lat={geo_coordinates.latitude}&lon={geo_coordinates.longitude}&appid={owm_key}'
        try:
            with urllib.request.urlopen(weather_url) as api_request:
                api_response = api_request.read().decode('utf-8')
                response_data = json.loads(api_response)
            api_request.close()
        except (ConnectionError, URLError) as ce:
            response_data = {'Error': 'Cannot connect to internet at the moment: {}'.format(ce)}
        except (ValueError, TypeError) as e:
            response_data = {'Error': 'Cannot interpret the response due to data or type mismatch: {}'.format(e)}

        # Prepare the final model object from the response json
        self.prepare_weather_data(response_data)
        return self.weather_data

    def prepare_weather_data(self, response_data) -> None:
        if 'Error' not in response_data.keys():
            # country
            self.weather_data.country = response_data['sys']['country']

            # icon-code for current conditions
            self.weather_data.icon_id = response_data['weather'][0]['icon']

            # wind
            self.weather_data.wind_speed = response_data['wind']['speed']
            self.weather_data.wind_degree = response_data['wind']['deg']

            # current conditions
            current_condition_desc = response_data['weather'][0]['description']
            # .title() capitalizes the 1st character of each word
            self.weather_data.condition_description = current_condition_desc.title()

            current_temperature = response_data['main']['temp']
            self.weather_data.general_temperature = self.scale_temperature(current_temperature, self.weather_data)
        else:
            current_temperature = 420.00
            self.weather_data.general_temperature = current_temperature

    def scale_temperature(self, current_temp, weather_data) -> float:
        """
        Helper method to convert the temperature from Kelvin Scale to Fahrenheit or Celsius depending on the metric
        system the given country uses.
        :param - WeatherModel
        :param - float (Kelvin)
        :return - float (Fahrenheit/Celsius)
        """
        if weather_data.country in imperial_countries:
            return (current_temp * (9 / 5)) - 459.67
        else:
            return current_temp - 273