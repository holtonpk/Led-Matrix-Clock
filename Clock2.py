from cgitb import reset
from operator import iconcat
import time
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics
from random import randint
from PIL import Image
import requests
import os

class Time:
    def get_time(self):
       
        date = datetime.now().strftime("%b %d")
        minute = datetime.now().minute
        if int(minute) < 10:
            minute = "0"+str(minute)
        hour = datetime.now().hour
        if int(hour) > 12:
            hour -= 12

        return {"hour":hour, "minute":minute, "date":date}


class Weather:
    def get_temp(self):
        response = requests.get('http://api.weatherapi.com/v1/current.json?key=1edec8319ff140bd898231802221106 &q=80126&aqi=no')
        return response.json()

        
class Display:
    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.brightness = 30

        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        self.matrix = RGBMatrix(options=options)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.prevtime = 0
        self.timeFont = graphics.Font()
        self.dateFont = graphics.Font(1)
        self.tempFont = graphics.Font(2)
        self.timeFont.LoadFont("./fonts/9x18B.bdf")
        self.dateFont.LoadFont("./fonts/7x13B.bdf")
        self.tempFont.LoadFont("./fonts/5x8.bdf")
    


    def displayDate(self, date):
        image1 = Image.open("./calendar.png")
        image1.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.offscreen_canvas.SetImage(image1.convert('RGB'), 2, 2)
        self.dateText =  graphics.DrawText(self.offscreen_canvas, self.dateFont,  (image1.width + 4), 12, graphics.Color(255, 0, 255), date)


    def displayTime(self, time):
       self.clockText =  graphics.DrawText(self.offscreen_canvas, self.timeFont,  1, 28, graphics.Color(255,255,255), str(time['hour'])+":"+str(time['minute']))


    def displayTemp(self, weather):

       
        imgPath = './weather/64x64'+(str(weather['current']['condition']['icon']).rsplit("64x64")[1])


        image2 = Image.open(imgPath)
        image2.thumbnail((40, 30), Image.ANTIALIAS) 


        self.offscreen_canvas.SetImage(image2.convert('RGB'), 40, 12)


        graphics.DrawText(self.offscreen_canvas, self.tempFont, self.clockText+13, 30, graphics.Color(0, 0, 0), str(round(weather['current']['temp_f']))+"°")


    def clear(self):
            self.offscreen_canvas.Clear()


    def config(self):
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        
 

if __name__ == "__main__":
    d = Display()
    time = {}
    weather = {}

    while True:
        current_weather = Weather().get_temp()
        current_time = Time().get_time()
        if time != current_time or weather != current_weather:
            d.clear()
            d.displayDate(current_time['date'])
            d.displayTime(current_time)
            time = current_time
            d.displayTemp(current_weather)
            weather = current_weather
            d.config()

      





        


    input("stop")

