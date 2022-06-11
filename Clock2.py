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
        self.font = graphics.Font()
        self.font2 = graphics.Font(1)
        self.font.LoadFont("./fonts/6x13B.bdf")
        self.font2.LoadFont("./fonts/7x13B.bdf")
    


    def display(self, data):
        color1 = randint(0,255)
        color2 = randint(0,255)
        color3 = randint(0,255)


        image1 = Image.open("./calendar.png")
        image1.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)



        Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2,  14, 13, graphics.Color(255, 255, 255), str("JUN 1"))

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        dateWidth = 32 - ( (image1.width + 2 + Dtxt) / 2)


        print(dateWidth)


        # time = str(data['hour'])+':'+str(data['minute'])
        # date = data['date']

        # Ttxt = graphics.DrawText(self.offscreen_canvas, self.font, 10, 15, graphics.Color(255, 255, 255), str("3:33"))

        self.offscreen_canvas.Clear()

        calIcon = self.offscreen_canvas.SetImage(image1.convert('RGB'), dateWidth, 2)
        Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2,  (dateWidth+image1.width + 2), 13, graphics.Color(255, 255, 255), str("JUN 1"))





        # self.offscreen_canvas.Clear()
        # timepos = 32 - (Ttxt / 2)
        # datepos = 32 - (Dtxt / 2)
        # Ttxt = graphics.DrawText(self.offscreen_canvas, self.font, timepos, 18, graphics.Color(color1), str(time))
        # Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2, datepos, 27, graphics.Color(color2), str(date))
        # self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        


if __name__ == "__main__":
    d = Display()
    time = {}
    # while True:
        # current_time = Time().get_time()
        # if time != current_time:
        #     d.display(current_time)
        #     time = current_time
    d.display({"hour":"3", "minute":'33', "date":'3/3'})
    input("stop")

