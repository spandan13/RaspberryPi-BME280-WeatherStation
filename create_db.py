import sqlite3
import sys
import config
con = sqlite3.connect(config.db_file)
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS weather_data")
    cur.execute("CREATE TABLE weather_data(timestamp DATETIME, wapi_temp NUMERIC, bme_temp NUMERIC, wapi_hum NUMERIC, bme_hum NUMERIC, wapi_pressure NUMERIC, bme_pressure NUMERIC, wapi_wind NUMERIC, wapi_wind_dir TEXT)")