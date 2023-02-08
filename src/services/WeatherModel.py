
class WeatherModel:
    def __init__(self):
        # setting these values with some defaults here - you are more than welcome to modify it to your interests.
        self._icon_id: str = "01d"
        self._general_temperature: float = 420.00
        self._condition_description: str = "Yee-haw"

        self._wind_speed: float = 420.69
        self._wind_direction: int = 0  # This will range from 0-359

        self._country: str = "US"

    @property
    def icon_id(self):
        return self._icon_id

    @icon_id.setter
    def icon_id(self, code):
        self._icon_id = code

    @property
    def general_temperature(self):
        return self._general_temperature

    @general_temperature.setter
    def general_temperature(self, current_temp):
        self._general_temperature = current_temp

    @property
    def condition_description(self):
        return self._condition_description

    @condition_description.setter
    def condition_description(self, cond_desc):
        self._condition_description = cond_desc

    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, win_spx):
        self._wind_speed = win_spx

    @property
    def wind_direction(self):
        return self._wind_direction

    @wind_direction.setter
    def wind_direction(self, win_dir):
        self._wind_direction = win_dir

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, cntry):
        self._country = cntry