#!/bin/python3

import bme_data_old
from flask import Flask, render_template

server_name = "OrbitSrv"

app = Flask(__name__)
@app.route("/")
def index():
    owm_humidity,owm_pressure,owm_temp,bme_humidity,bme_pressure,bme_temp,altitude = bme_data_old.get_all_data()
    return render_template("index.html",server_name=server_name,o_hu=owm_humidity,hu=round(bme_humidity,2),o_pre=owm_pressure,pre=round(bme_pressure,2),o_temp=owm_temp,temp=round(bme_temp,2),alti=round(altitude,2))

app.run(host="0.0.0.0", port=6162)

