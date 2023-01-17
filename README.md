<h1 align="center">
    RaspberryPi-BME280-WeatherStation

  <br>
  <img src="https://i.imgur.com/2Lwfekl.png" alt="dashboard"></a>
  <br>
</h1>

## If you always wondered what the temperature inside your home was, this is for you!

## Time to set-up your own indoor weather station!
***
## *Requirements:*

![bme280 sensor](https://i.imgur.com/pIHbhJM.png)
BME280 Sensor

RaspberryPi Zero/2 W, 3,4
(Not yet tested on Pi 1,2 but should work I guess?)

[WeatherAPI](https://www.weatherapi.com/)
***
## *Set-up:*

Connect the sensor to the Pi

| Pi GPIO | BME280 |
| ------- | ------ |
| 17 (3V3) | Vin |
| 6 (Gnd) | Gnd |
| 3 (SDA) | SDA (SDI) |
| 5 (SCL) | SCL (SCK) |

If you happen to already have some other i2c device/sensor/display connected to pin 3,5 then you can enable another i2c bus by adding the following line to your `/boot/config.txt` file:

`dtoverlay=i2c-gpio,bus=2,i2c_gpio_sda=22,i2c_gpio_scl=23`

And then you can connect the sda and scl to the above mention gpio pins (Pin 15,16 in this case)
***
## *Installation:*

Clone this repository:
`git clone https://github.com/spandan13/RaspberryPi-BME280-WeatherStation.git`

Make sure you have sqlite3 installed:
`sudo apt install sqlite3`

CD to the cloned repo and install the requirements:
`pip3 install -r requirements.txt`

Open the sample-settings file and set the values:

| Setting | Value |
| ------- | ----- |
| lat | Your location lattitude |
| lon | Your location longitute |
| api\_key | Your OpenWeatherMap API Key |
| port | Default is 1 but needs to be changed to 2 if set new bus in config.txt |
| address | Default is 0x76, Some BME280 use 0x77 |
| server\_name | Whatever name you want the Dashboard to show |
| server\_port | Port for the web dashboard |
| db\_file | Full path to database file. The file will be created if it does not exist |

**Rename the `sample-settings` file to `settings`**
***
### **We can now test to see if the sensor works:**

`python3 bme-test.py`

If you see Temp, Humidity and Pressure values returned then you're good to go!

Now, we need to create db file and the required table to store the values:
`python3 create_db.py`

And now we need to set-up a cron job that will log values to the db at the interval you set.
Add below line to your cron file `crontab -e` (This logs every 5 minutes)

`*/5 * * * * cd /full/path/to/repo/ && python3 log_to_db.py`
***
### **We are now done with the installation, time to run the full app:**

`python3 bme_app.py`

Navigate to http://your-pi-ip:port and you should see the dashboard up and running!

### **Finally you have cured your curiosity to know what your actual indoor temperature is vs what you see online!**

