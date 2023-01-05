import bme280
import smbus2
import requests
import math

# Config for BME280 Sensor
port = 2
address = 0x76 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

# Config for OpenWeatherMap API
lat = "19.367738"
lon = "72.7965333"
api_key = "e6ab838e58e11e0a698c0a606a42d0ae"

def bme_data():
    bme280_data = bme280.sample(bus,address)
    humidity  = bme280_data.humidity
    pressure  = bme280_data.pressure
    ambient_temperature = bme280_data.temperature
    
    return humidity, pressure, ambient_temperature

def owm_data():
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}").json()
    temp = (int(weather_data['main']['temp']-273.15))
    pressure = (int(weather_data['main']['pressure']))
    humidity = (int(weather_data['main']['humidity']))
    
    return humidity, pressure, temp

def get_all_data():
    owm_humidity,owm_pressure,owm_temp = owm_data()
    bme_humidity,bme_pressure,bme_temp = bme_data()
    altitude = 44330 * (1.0 - math.pow(bme_pressure / owm_pressure, 0.1903))
    
    return owm_humidity,owm_pressure,owm_temp,bme_humidity,bme_pressure,bme_temp,altitude