#!/bin/python3

import sqlite3
import weather_data
import re
from flask import Flask, render_template

server_name = "OrbitSrv"

conn = sqlite3.connect('/home/orbitsrv/Documents/code/bme280-web-app/my_weather.db', check_same_thread=False)
curs = conn.cursor()

def parse_db():
    for row in curs.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1"):
        owm_temp = row[1]
        bme_temp = row[2]
        owm_humidity = row[3]
        bme_humidity = row[4]
        owm_pressure = row[5]
        bme_pressure = row[6]
        altitude = row[7]
    conn.close()
    return owm_humidity,owm_pressure,owm_temp,bme_humidity,bme_pressure,bme_temp,altitude

def getHistData(numSamples):
    try:
        curs.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
    except:
        conn = sqlite3.connect('/home/orbitsrv/Documents/code/bme280-web-app/new_Weather.db', check_same_thread=False)
        curs = conn.cursor()
        curs.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
    dates = []
    owm_temps = []
    bme_temps = []
    owm_hums = []
    bme_hums = []
    owm_pres = []
    bme_pres = []
    altis = []
    for row in reversed(data):
        dates.append(re.sub("^(\d{4})-(\d{2})-(\d{2})\s", "", row[0]))
        owm_temps.append(row[1])
        bme_temps.append(row[2])
        owm_hums.append(row[3])
        bme_hums.append(row[4])
        owm_pres.append(row[5])
        bme_pres.append(row[6])
        altis.append(row[7])
    
    return dates, owm_temps, bme_temps, owm_hums, bme_hums, owm_pres, bme_pres, altis

def maxRowsTable():
	for row in curs.execute("select COUNT(owm_temp) from  weather_data"):
		maxNumberRows=row[0]
	return maxNumberRows

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if numSamples > 13:
    numSamples = 13

app = Flask(__name__)
@app.route("/")
def index():
    owm_humidity,owm_pressure,owm_temp,bme_humidity,bme_pressure,bme_temp,altitude = weather_data.get_all_data()
    dates, owm_temps, bme_temps, owm_hums, bme_hums, owm_pres, bme_pres, altis = getHistData(numSamples)
    conn.close()
    return render_template("index.html",server_name=server_name,o_hu=owm_humidity,
                           hu=round(bme_humidity,2),o_pre=owm_pressure,pre=round(bme_pressure,2),
                           o_temp=owm_temp,temp=round(bme_temp,2),alti=round(altitude,2),
                           dates=dates, owm_temps=owm_temps, bme_temps=bme_temps, owm_hums=owm_hums,
                           bme_hums=bme_hums, owm_pres=owm_pres, bme_pres=bme_pres, altis=altis)

app.run(host="0.0.0.0", port=6162)

