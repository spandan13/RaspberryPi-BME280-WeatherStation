import configparser
import ast

config = configparser.ConfigParser()
config.read("settings")

owm_config = config['OpenWeatherMap']
lat = owm_config['lat']
lon = owm_config['lon']
api_key = owm_config['api_key']

bme_config = config['bme_sensor']
port = int(bme_config['port'])
address = ast.literal_eval(bme_config['address'])

other = config['Other']
server_name = other['server_name']
server_port = int(other['server_port'])
db_file = other['db_file']