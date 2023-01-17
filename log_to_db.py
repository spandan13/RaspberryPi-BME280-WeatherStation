import sqlite3
import weather_data
import config

db_file = config.db_file
conn=sqlite3.connect(db_file)
curs=conn.cursor()
# function to insert data on a table
def add_data (wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp):
    curs.execute("INSERT INTO weather_data values(datetime('now','localtime'), (?), (?), (?), (?), (?), (?), (?), (?))",
                 (wapi_temp,bme_temp,wapi_humidity,bme_humidity,wapi_pressure,bme_pressure,wapi_wind,wapi_wind_dir))
    conn.commit()
    conn.close()
    
wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp = weather_data.get_all_data()
add_data(wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,round(bme_humidity,2),round(bme_pressure,2),round(bme_temp,2))
