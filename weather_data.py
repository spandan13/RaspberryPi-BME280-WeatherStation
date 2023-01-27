import bme280
import smbus2
import requests
import math
import config

# Config for BME280 Sensor. Modify in settings file
port = config.port
address = config.address
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

# Config for OpenWeatherMap API. Modify in settings file
lat = config.lat
lon = config.lon
api_key = config.api_key

def bme_data():
    bme280_data = bme280.sample(bus,address)
    humidity  = bme280_data.humidity
    pressure  = bme280_data.pressure
    ambient_temperature = bme280_data.temperature
    
    return humidity, pressure, ambient_temperature

def wapi_data():
    weather_data = requests.get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}&aqi=yes").json()
    temp = int(weather_data['current']['temp_c'])
    pressure = int(weather_data['current']['pressure_mb'])
    humidity = int(weather_data['current']['humidity'])
    wind = int(weather_data['current']['wind_kph'])
    wind_dir = weather_data['current']['wind_dir']
    
    return humidity, pressure, temp, wind, wind_dir

def get_all_data():
    wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir = wapi_data()
    bme_humidity,bme_pressure,bme_temp = bme_data()
    
    return wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp
