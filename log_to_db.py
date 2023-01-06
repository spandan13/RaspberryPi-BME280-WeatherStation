import sqlite3
import weather_data
import config

db_file = config.db_file
conn=sqlite3.connect(db_file)
curs=conn.cursor()
# function to insert data on a table
def add_data (owm_humidity,owm_pressure,owm_temp,bme_humidity,bme_pressure,bme_temp,altitude):
    curs.execute("INSERT INTO weather_data values(datetime('now','localtime'), (?), (?), (?), (?), (?), (?), (?))",
                 (owm_temp,bme_temp,owm_humidity,bme_humidity,owm_pressure,bme_pressure,altitude))
    conn.commit()
    conn.close()
    
owm_humidity,owm_pressure,owm_temp,bme_humidity,bme_pressure,bme_temp,altitude = weather_data.get_all_data()
add_data(owm_humidity,owm_pressure,owm_temp,round(bme_humidity,2),round(bme_pressure,2),round(bme_temp,2),round(altitude,2))
