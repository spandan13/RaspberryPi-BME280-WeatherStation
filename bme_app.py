#!/bin/python3

import sqlite3
import weather_data
import re
import config
from flask import Flask, render_template

server_name = config.server_name
server_port = config.server_port
db_file = config.db_file
conn = sqlite3.connect(db_file, check_same_thread=False)
curs = conn.cursor()

def parse_db():
    """This function is not currenty being used but is here in case
        you wish to pull results from the db instead of querying the
        api and the sensor everytime you refresh the page"""
    for row in curs.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1"):
        wapi_temp = row[1]
        bme_temp = row[2]
        wapi_humidity = row[3]
        bme_humidity = row[4]
        wapi_pressure = row[5]
        bme_pressure = row[6]
        wapi_wind = row[7]
        wapi_wind_dir = row[8]
    return wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp,altitude

def getHistData(numSamples):
    try:
        curs.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
    except:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        curs = conn.cursor()
        curs.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
    dates = []
    wapi_temps = []
    bme_temps = []
    wapi_hums = []
    bme_hums = []
    wapi_pres = []
    bme_pres = []
    wapi_winds = []
    for row in reversed(data):
        dates.append(re.sub("^(\d{4})-(\d{2})-(\d{2})\s", "", row[0]))
        wapi_temps.append(row[1])
        bme_temps.append(row[2])
        wapi_hums.append(row[3])
        bme_hums.append(row[4])
        wapi_pres.append(row[5])
        bme_pres.append(row[6])
        wapi_winds.append(row[7])
    
    return dates, wapi_temps, bme_temps, wapi_hums, bme_hums, wapi_pres, bme_pres, wapi_winds

def maxRowsTable():
	for row in curs.execute("select COUNT(wapi_temp) from  weather_data"):
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
    wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp = weather_data.get_all_data()
    # To use results from db, comment above line and uncomment below line
    # wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp,altitude = parse_db()
    dates, wapi_temps, bme_temps, wapi_hums, bme_hums, wapi_pres, bme_pres, wapi_winds = getHistData(numSamples)
    conn.close()
    return render_template("index.html",server_name=server_name,o_hu=wapi_humidity,
                           hu=round(bme_humidity,2),o_pre=wapi_pressure,pre=round(bme_pressure,2),
                           o_temp=wapi_temp,temp=round(bme_temp,2),o_wind=wapi_wind,o_wind_dir=wapi_wind_dir,
                           dates=dates, wapi_temps=wapi_temps, bme_temps=bme_temps, wapi_hums=wapi_hums,
                           bme_hums=bme_hums, wapi_pres=wapi_pres, bme_pres=bme_pres, wapi_winds=wapi_winds)

app.run(host="0.0.0.0", port=server_port)
