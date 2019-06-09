from datetime import datetime, timedelta

from homeassistant.components.weather import (
    WeatherEntity, ATTR_FORECAST_CONDITION, ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TEMP, ATTR_FORECAST_TEMP_LOW, ATTR_FORECAST_TIME, ATTR_FORECAST_WIND_BEARING, ATTR_FORECAST_WIND_SPEED)
from homeassistant.const import (TEMP_CELSIUS, TEMP_FAHRENHEIT, CONF_API_KEY, CONF_API_VERSION, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME)

import requests
import json

VERSION = '0.1'
DOMAIN = 'colorfulclouds'

# mapping, why? because 
# https://github.com/home-assistant/home-assistant-polymer/blob/master/src/cards/ha-weather-card.js#L279
# https://open.caiyunapp.com/%E5%BD%A9%E4%BA%91%E5%A4%A9%E6%B0%94_API/v2.5

CONDITION_MAP = {
    'CLEAR_DAY': 'sunny',
    'CLEAR_NIGHT': 'clear-night',
    'PARTLY_CLOUDY_DAY': 'partlycloudy',
    'PARTLY_CLOUDY_NIGHT':'partlycloudy',
    'CLOUDY': 'cloudy',
    'LIGHT_HAZE': 'fog',
    'MODERATE_HAZE': 'fog',
    'HEAVY_HAZE': 'fog',
    'LIGHT_RAIN': 'rainy',
    'MODERATE_RAIN': 'rainy',
    'HEAVY_RAIN': 'pouring',
    'STORM_RAIN': 'pouring',
    'FOG': 'fog',
    'LIGHT_SNOW': 'snowy',
    'MODERATE_SNOW': 'snowy',
    'HEAVY_SNOW': 'snowy',
    'STORM_SNOW': 'snowy',
    'DUST': 'fog',
    'SAND': 'fog',
    'THUNDER_SHOWER': 'lightning-rainy',
    'HAIL': 'hail',
    'SLEET': 'snowy-rainy',
    'WIND': 'windy',
    'HAZE': 'fog',
    'RAIN': 'rainy',
    'SNOW': 'snowy'
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([ColorfulCloudsWeather(api_key=config.get(CONF_API_KEY),
                                        api_version=config.get(CONF_API_VERSION, 'v2.5'),
                                        lng=config.get(CONF_LONGITUDE, hass.config.longitude),
                                        lat=config.get(CONF_LATITUDE, hass.config.latitude),
                                        name=config.get(CONF_NAME, 'colorfulclouds'))])


class ColorfulCloudsWeather(WeatherEntity):
    """Representation of a weather condition."""

    def __init__(self, api_key: str, api_version: str, lng: str, lat: str, name: str):
        self._api_key = api_key
        self._api_version = api_version
        self._lng = lng
        self._lat = lat
        self._name = name

        self.update()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        """Return the weather condition."""
        skycon = self._realtime_data['result']['realtime']['skycon']
        return CONDITION_MAP[skycon]

    @property
    def temperature(self):
        return self._realtime_data['result']['realtime']['temperature']

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def humidity(self):
        return float(self._realtime_data['result']['realtime']['humidity']) * 100

    @property
    def wind_speed(self):
        """风速"""
        return self._realtime_data['result']['realtime']['wind']['speed']

    @property
    def wind_bearing(self):
        """风向"""
        return self._realtime_data['result']['realtime']['wind']['direction']

    @property
    def visibility(self):
        """能见度"""
        return self._realtime_data['result']['realtime']['visibility']

    @property
    def pressure(self):
        return self._realtime_data['result']['realtime']['pressure']

    @property
    def attribution(self):
        """Return the attribution."""
        return 'Powered by ColorfulClouds and China Meteorological Administration'

    @property
    def pm25(self):
        """pm25，质量浓度值"""
        return self._realtime_data['result']['realtime']['air_quality']['pm25']

    @property
    def pm10(self):
        """pm10，质量浓度值"""
        return self._realtime_data['result']['realtime']['air_quality']['pm10']
    
    @property
    def o3(self):
        """臭氧，质量浓度值"""
        return self._realtime_data['result']['realtime']['air_quality']['o3']

    @property
    def no2(self):
        """二氧化氮，质量浓度值"""
        return self._realtime_data['result']['realtime']['air_quality']['no2']

    @property
    def so2(self):
        """二氧化硫，质量浓度值"""
        return self._realtime_data['result']['realtime']['air_quality']['so2']

    @property
    def co(self):
        """一氧化碳，质量浓度值"""
        return self._realtime_data['result']['realtime']['air_quality']['co']

    @property
    def aqi(self):
        """AQI（国标）"""
        return self._realtime_data['result']['realtime']['air_quality']['aqi']['chn']
    
    @property
    def aqi_description(self):
        """AQI（国标）"""
        return self._realtime_data['result']['realtime']['air_quality']['description']['chn']

    @property
    def aqi_usa(self):
        """AQI USA"""
        return self._realtime_data['result']['realtime']['air_quality']['aqi']['usa']
    
    @property
    def aqi_usa_description(self):
        """AQI USA"""
        return self._realtime_data['result']['realtime']['air_quality']['description']['usa']

    @property
    def state_attributes(self):
        data = super(ColorfulCloudsWeather, self).state_attributes
        data['pm25'] = self.pm25
        data['pm10'] = self.pm10
        data['o3'] = self.o3
        data['no2'] = self.no2
        data['so2'] = self.so2
        data['co'] = self.co
        data['aqi'] = self.aqi
        data['aqi_description'] = self.aqi_description
        data['aqi_usa'] = self.aqi_usa
        data['aqi_usa_description'] = self.aqi_usa_description
        return data  

    @property
    def forecast(self):
        forecast_data = []
        for i in range(5):
            time_str = self._forecast_data['result']['daily']['temperature'][i]['date'][:10]
            data_dict = {
                ATTR_FORECAST_TIME: datetime.strptime(time_str, '%Y-%m-%d'),
                ATTR_FORECAST_CONDITION: CONDITION_MAP[self._forecast_data['result']['daily']['skycon'][i]['value']],
                ATTR_FORECAST_PRECIPITATION: self._forecast_data['result']['daily']['precipitation'][i]['avg'],
                ATTR_FORECAST_TEMP: self._forecast_data['result']['daily']['temperature'][i]['avg'],
                ATTR_FORECAST_TEMP_LOW: self._forecast_data['result']['daily']['temperature'][i]['min'],
                ATTR_FORECAST_WIND_BEARING: self._forecast_data['result']['daily']['wind'][i]['avg']['direction'],
                ATTR_FORECAST_WIND_SPEED: self._forecast_data['result']['daily']['wind'][i]['avg']['speed']
            }
            forecast_data.append(data_dict)

        return forecast_data

    def update(self):
        json_text = requests.get(str.format("https://api.caiyunapp.com/{}/{}/{},{}/realtime.json?unit=metric:v2", self._api_version, self._api_key, self._lng, self._lat)).content
        self._realtime_data = json.loads(json_text)

        json_text = requests.get(str.format("https://api.caiyunapp.com/{}/{}/{},{}/forecast.json?unit=metric:v2", self._api_version, self._api_key, self._lng, self._lat)).content
        self._forecast_data = json.loads(json_text)
