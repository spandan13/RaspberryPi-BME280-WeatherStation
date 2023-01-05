#!/bin/python3

import requests
import math
from bme_data import BME280Module
from flask import Flask, render_template

lat = "19.367738"
lon = "72.7965333"
api_key = "e6ab838e58e11e0a698c0a606a42d0ae"
server_name = "OrbitSrv"

def outdoors_weather():
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}").json()
    temp = (int(weather_data['main']['temp']-273.15))
    pressure = (int(weather_data['main']['pressure']))
    humidity = (int(weather_data['main']['humidity']))
    
    return humidity,pressure,temp

bme280_module = BME280Module()

app = Flask(__name__)
@app.route("/")
def index():
    out_humidity,out_pressure,out_temp = outdoors_weather()
    humidity,pressure,temp = bme280_module.get_sensor_readings()
    altitude = 44330 * (1.0 - math.pow(pressure / out_pressure, 0.1903))
    return render_template("index.html",server_name=server_name,o_hu=out_humidity,hu=round(humidity,2),o_pre=out_pressure,pre=round(pressure,2),o_temp=out_temp,temp=round(temp,2),alti=round(altitude,2))

app.run(host="0.0.0.0", port=6162)

