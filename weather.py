import requests

import math

zip = '80126'

response = requests.get('http://api.weatherapi.com/v1/current.json?key=1edec8319ff140bd898231802221106 &q=80126&aqi=no')
weather = response.json()


path = './weather/64x64'+ (str(weather['current']['condition']['icon']).rsplit("64x64")[1])
print(path )