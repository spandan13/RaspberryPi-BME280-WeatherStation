import sqlite3
import sys
import config
con = sqlite3.connect('testFinalWeather.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS weather_data")
    cur.execute("CREATE TABLE weather_data(timestamp DATETIME, owm_temp NUMERIC, bme_temp NUMERIC, owm_hum NUMERIC, bme_hum NUMERIC, owm_pressure NUMERIC, bme_pressure NUMERIC, altitude NUMERIC)")