import time
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics
from random import randint



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
        self.font = graphics.Font()
        self.font2 = graphics.Font(1)
        self.font.LoadFont("./10x20.bdf")
        self.font2.LoadFont("./6x9.bdf")
    


    def display(self, data):
        color1 = randint(0,255)
        color2 = randint(0,255)
        color3 = randint(0,255)

        time = str(data['hour'])+':'+str(data['minute'])
        date = data['date']

        Ttxt = graphics.DrawText(self.offscreen_canvas, self.font, 10, 18, graphics.Color(0, 0, 255),
                                      str(time))
        Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2, 10, 27, graphics.Color(0, 0, 255),
                                      str(date))
        self.offscreen_canvas.Clear()
        timepos = 32 - (Ttxt / 2)
        datepos = 32 - (Dtxt / 2)
        Ttxt = graphics.DrawText(self.offscreen_canvas, self.font, timepos, 18, graphics.Color(color1, color2, color3),
                                      str(time))
        Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2, datepos, 27, graphics.Color(255-color1, 255-color2, 255-color3),
                                      str(date))
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        


if __name__ == "__main__":
    d = Display()
    time = {}
    while True:
        current_time = Time().get_time()
        if time != current_time:
            d.display(current_time)
            time = current_time
