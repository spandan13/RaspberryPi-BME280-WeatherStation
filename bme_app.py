#!/bin/python3

import sqlite3
import weather_data
import re
import config
from flask import Flask, render_template
from datetime import datetime, timedelta

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

def calc_avg(temps):
    filtered_temps = [i for i in temps if i != 0]
    total = 0
    for temp in filtered_temps:
        total += temp
    try:
        average = total / len(filtered_temps)
    except ZeroDivisionError:
        average = 0
    return average

def get_avg_data(all_dates):
    dates = []
    bme_avgs = []
    wapi_avgs = []
    bme_temps = []
    wapi_temps = []
    for date in all_dates:
        dates.append(date)
        try:
            data = curs.execute(f"SELECT bme_temp,wapi_temp FROM weather_data WHERE timestamp LIKE '%{date}%';")
        except:
            conn = sqlite3.connect(db_file, check_same_thread=False)
            curs = conn.cursor()
            data = curs.execute(f"SELECT bme_temp,wapi_temp FROM weather_data WHERE timestamp LIKE '%{date}%';") 
        for row in data:
            bme_temps.append(row[0])
            wapi_temps.append(row[1])
        bme_average = calc_avg(bme_temps)
        wapi_average = calc_avg(wapi_temps)
        bme_avgs.append(round(bme_average,2))
        wapi_avgs.append(round(wapi_average,2))
    if len(bme_avgs) == 0:
        bme_avgs.append("0")
    if len(wapi_avgs) == 0:
        wapi_avgs.append("0")
    return dates,bme_avgs,wapi_avgs

def last_seven_dates():
    dates_list = []
    today = datetime.today()
    for i in range(7):
        date = today - timedelta(days=i)
        dates_list.append(date.strftime("%Y-%m-%d"))
    daily,daily_bme_avgs,daily_wapi_avgs = get_avg_data(dates_list)
    daily.reverse()
    daily_bme_avgs.reverse()
    daily_wapi_avgs.reverse()
    return daily, daily_bme_avgs, daily_wapi_avgs

def last_four_weeks():
    today = datetime.today()
    dts = [0,7,14,21,28]
    dates_list = []
    week = []
    week_bme_avg = []
    week_wapi_avg = []
    for days in dts:
        week_start = today - timedelta(days=today.weekday() + days)
        week_end = week_start + timedelta(days=6)
        current_date = week_start
        while current_date <= week_end:
            dates_list.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
        dates,bme_avgs,wapi_avgs = get_avg_data(dates_list)
        bme_average = calc_avg(bme_avgs)
        wapi_average = calc_avg(wapi_avgs)
        week.append(f"{dates_list[0]} to {dates_list[-1]}")
        week_bme_avg.append(round(bme_average,2))
        week_wapi_avg.append(round(wapi_average,2))
        dates_list.clear()
    week.reverse()
    week_bme_avg.reverse()
    week_wapi_avg.reverse()
    return week,week_bme_avg,week_wapi_avg
    
def last_twelve_month():
    today = datetime.today()
    dts = [0,1,32,64,96,128,160,192,224,256,288,320,352]
    dates_list = []
    month = []
    month_bme_avg = []
    month_wapi_avg = []
    for days in dts:
        first_day_of_current_month = today.replace(day=1)
        last_month = first_day_of_current_month - timedelta(days=days)
        first_day_of_last_month = last_month.replace(day=1)
        total_days = [31,30,29,28]
        for days in total_days:
            try:
                last_day_of_current_month = last_month.replace(day=days)
                break
            except ValueError:
                continue
        last_month_range = (first_day_of_last_month + timedelta(n) for n in range((last_day_of_current_month - first_day_of_last_month).days + 1))
        for date in last_month_range:
            dates_list.append(date.strftime("%Y-%m-%d"))
        dates,bme_avgs,wapi_avgs = get_avg_data(dates_list)
        bme_average = calc_avg(bme_avgs)
        wapi_average = calc_avg(wapi_avgs)
        curr_month = (datetime.strptime(dates[0], '%Y-%m-%d')).strftime("%B %Y")
        month.append(curr_month)
        month_bme_avg.append(round(bme_average,2))
        month_wapi_avg.append(round(wapi_average,2))
        dates_list.clear()
    month.reverse()
    month_bme_avg.reverse()
    month_wapi_avg.reverse()
    return month,month_bme_avg,month_wapi_avg

app = Flask(__name__)
@app.route("/")
def index():
    wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp = weather_data.get_all_data()
    # To use results from db, comment above line and uncomment below line
    # wapi_humidity,wapi_pressure,wapi_temp,wapi_wind,wapi_wind_dir,bme_humidity,bme_pressure,bme_temp,altitude = parse_db()
    dates, wapi_temps, bme_temps, wapi_hums, bme_hums, wapi_pres, bme_pres, wapi_winds = getHistData(numSamples)
    daily,daily_bme_avgs,daily_wapi_avgs = last_seven_dates()
    week,week_bme_avg,week_wapi_avg = last_four_weeks()
    month,month_bme_avg,month_wapi_avg = last_twelve_month()
    conn.close()
    return render_template("index.html",server_name=server_name,o_hu=wapi_humidity,
                           hu=round(bme_humidity,2),o_pre=wapi_pressure,pre=round(bme_pressure,2),
                           o_temp=wapi_temp,temp=round(bme_temp,2),o_wind=wapi_wind,o_wind_dir=wapi_wind_dir,
                           dates=dates, wapi_temps=wapi_temps, bme_temps=bme_temps, wapi_hums=wapi_hums,
                           bme_hums=bme_hums, wapi_pres=wapi_pres, bme_pres=bme_pres, wapi_winds=wapi_winds,
                           daily=daily, daily_bme_avgs=daily_bme_avgs, daily_wapi_avgs=daily_wapi_avgs,
                           week=week, week_bme_avg=week_bme_avg, week_wapi_avg=week_wapi_avg,
                           month=month, month_bme_avg=month_bme_avg, month_wapi_avg=month_wapi_avg)

app.run(host="0.0.0.0", port=server_port)
