from operator import iconcat
import time
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics
from random import randint
from PIL import Image
import requests


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
        return round(response.json()['current']['temp_f'])

        
class Display:
    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
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
        self.dateFont.LoadFont("./fonts/6x13B.bdf")
        self.tempFont.LoadFont("./fonts/6x9.bdf")
    


    def displayDate(self, date):
        image1 = Image.open("./calendar.png")
        image1.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.offscreen_canvas.SetImage(image1.convert('RGB'), 2, 2)
        self.dateText =  graphics.DrawText(self.offscreen_canvas, self.dateFont,  (image1.width + 4), 12, graphics.Color(255, 255, 255), date)


    def displayTime(self, time):
       self.clockText =  graphics.DrawText(self.offscreen_canvas, self.timeFont,  1, 28, graphics.Color(255, 255, 255), str(time['hour'])+":"+str(time['minute']))


    def displayTemp(self, temp):
        graphics.DrawText(self.offscreen_canvas, self.tempFont, self.clockText+9, 30, graphics.Color(255, 255, 255), temp)



    def config(self):
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        


if __name__ == "__main__":
    d = Display()
    time = {}
    weather = {}
    while True:
        current_weather = Weather().get_temp()
        current_time = Time().get_time()
        if time != current_time:
            d.displayDate(current_time['date'])
            d.displayTime(current_time)
            time = current_time
        if weather != current_weather:
            d.displayTemp(str(current_weather)+"°")
            weather = current_weather
        
        d.config()
        


    input("stop")

