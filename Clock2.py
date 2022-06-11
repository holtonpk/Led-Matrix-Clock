from operator import iconcat
import time
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics
from random import randint
from PIL import Image



class Time:
    def get_time(self):
        month = datetime.now().date().month
        day = datetime.now().date().day
        date = str(month) + '/' + str(day)
        minute = datetime.now().minute
        if int(minute) < 10:
            minute = "0"+str(minute)
        hour = datetime.now().hour
        if int(hour) > 12:
            hour -= 12

        return {"hour":hour, "minute":minute, "date":date}

        
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
        self.tempFont.LoadFont("./fonts/7x13B.bdf")
    


    def displayDate(self, date):
        image1 = Image.open("./calendar.png")
        image1.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.offscreen_canvas.SetImage(image1.convert('RGB'), 2, 2)
        self.dateText =  graphics.DrawText(self.offscreen_canvas, self.dateFont,  (image1.width + 4), 12, graphics.Color(255, 255, 255), date)


    def displayTime(self, time):
       self.clockText =  graphics.DrawText(self.offscreen_canvas, self.timeFont,  2, 26, graphics.Color(255, 255, 255), time)


    def displayTemp(self, temp):
        graphics.DrawText(self.offscreen_canvas, self.tempFont, self.clockText+2, 34, graphics.Color(255, 255, 255), temp)



    def config(self):
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        


if __name__ == "__main__":
    d = Display()
    time = {}
    # while True:
        # current_time = Time().get_time()
        # if time != current_time:
        #     d.display(current_time)
        #     time = current_time
    d.displayDate("Jun 10")
    d.displayTime("9:00")
    d.displayTemp("75°")
    d.config()
    input("stop")

