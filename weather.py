import requests



zip = '80126'

response = requests.get('http://api.weatherapi.com/v1/current.json?key=1edec8319ff140bd898231802221106 &q=80126&aqi=no')

print('weather:',response.json()['current']['temp_f'])