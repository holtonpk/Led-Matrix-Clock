import requests

import math

zip = '80126'

response = requests.get('http://api.weatherapi.com/v1/current.json?key=1edec8319ff140bd898231802221106 &q=80126&aqi=no')
temperature = round( response.json()['current']['temp_f'])
print('weather:',temperature )