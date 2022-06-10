import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import os
from web3 import Web3
from rgbmatrix import graphics
from random import randint
from datetime import datetime
from tda import auth, client
import config
import b
import sys


class Time:
    def get_date(self):
        return str(datetime.now().date().month) + '/' + str(datetime.now().date().day)

    def get_minute(self):
        minute = datetime.now().minute
        if int(self.minute) < 10:
            minute = "0"+str(self.minute)
        return minute

    def get_hour(self):
        hour = datetime.now().hour
        if int(hour) > 12:
            hour -= 12
        return hour

    def get_time(self):
        minute = datetime.now().minute
        hour = datetime.now().hour
        if int(hour) > 12:
            hour -= 12
        if int(minute) < 10:
            minute = "0"+str(minute)
        return str(hour) + ":" + str(minute)


class data:
    def get_tokens(self):
        abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],' \
              '"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},' \
              '{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80",' \
              '"name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},' \
              '{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},' \
              '{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},' \
              '{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound",' \
              '"type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":' \
              '"view","type":"function"}]'
        CoinList = [{"TOKEN": "BTC", "ADDR": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",
                     "IMG":"/home/pi/Token_icons/btc.png", "Color":255,"Color1":145,"Color2":15},
                    {"TOKEN": "ETH", "ADDR": "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
                     "IMG":"/home/pi/Token_icons/eth.png", "Color":69,"Color1":74,"Color2":117},
                    {"TOKEN": "AAVE", "ADDR": "0x547a514d5e3769680Ce22B2361c10Ea13619e8a9",
                     "IMG":"/home/pi/Token_icons/aave.png", "Color":64,"Color1":172,"Color2":193},
                    {"TOKEN": "SOL", "ADDR": "0x4ffC43a60e009B551865A93d232E33Fce9f01507",
                     "IMG":"/home/pi/Token_icons/sol.png", "Color":193,"Color1":58,"Color2":244},
                    {"TOKEN": "LINK", "ADDR": "0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c",
                     "IMG":"/home/pi/Token_icons/link.png", "Color":51,"Color1":93,"Color2":210},
                    {"TOKEN": "ADA", "ADDR": "0xAE48c91dF1fE419994FFDa27da09D5aC69c30f55",
                     "IMG":"/home/pi/Token_icons/ada.png", "Color":0,"Color1":52,"Color2":173},
                    {"TOKEN": "AVAX", "ADDR": "0xFF3EEb22B5E3dE6e705b44749C2559d704923FD7",
                     "IMG":"/home/pi/Token_icons/avax.png", "Color":232,"Color1":65,"Color2":66}
                    ]
        textlist = []
        for coin in CoinList:
            textlist.append({'text': str(coin.get("TOKEN")) + " $" + str(round(int(Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/dfb29047e37a436fbbf8e723722f3b9c')).eth.contract(address=coin.get("ADDR"), abi=abi).functions.latestRoundData().call()[1]) / 100000000, 2)),
                            'Color1': coin.get("Color"), 'Color2': coin.get("Color1"),
                            'Color3': coin.get("Color2"), 'IMG':coin.get("IMG")})
        return textlist


    def get_stocks(self, _watchlist):
        c = auth.client_from_token_file(config.token_path, config.api_key, asyncio=False)
        Tickerlist = []
        for x in c.get_watchlists_for_single_account(config.account_id).json():
            if x['name'] == _watchlist:
                for stocks in x['watchlistItems']: Tickerlist.append(stocks.get('instrument').get('symbol'))
        textlist = []
        for tickers in Tickerlist:
            current = c.get_quote(tickers).json().get(tickers).get('lastPrice')
            percentchange = str(round((1 - (float(c.get_quote(tickers).json().get(tickers).get('closePrice')) / float(current))) * 100, 2))
            if float(percentchange) > 0:
                color1 = 0
                color2 = 255
                color3 = 0
                img = '/home/pi/Token_icons/up.png'
            else:
                color1 = 255
                color2 = 0
                color3 = 0
                img = '/home/pi/Token_icons/down.png'

            textlist.append({'text': tickers + ' ' + percentchange + '%'+' $ ' + str(current), 'Color1': color1,
                            'Color2': color2, 'Color3': color3, 'IMG': img
                            })
        return textlist

class clock:

    def print_Clock(self, Pos1, Pos2):
        self.Ttxt = graphics.DrawText(ledBoard.offscreen_canvas, ledBoard.font, 10, Pos1, graphics.Color(0, 0, 255),
                                      str(Time().get_time()))
        self.Dtxt = graphics.DrawText(ledBoard.offscreen_canvas, ledBoard.font2, 10, Pos2, graphics.Color(0, 0, 255),
                                      str(Time().get_date()))
        ledBoard.offscreen_canvas.Clear()
        self.timepos = 32 - (self.Ttxt / 2)
        self.datepos = 32 - (self.Dtxt / 2)
        self.Ttxt = graphics.DrawText(ledBoard.offscreen_canvas, ledBoard.font, self.timepos, Pos1, graphics.Color(0, 0, 255),
                                      str(Time().get_time()))
        self.Dtxt = graphics.DrawText(ledBoard.offscreen_canvas, ledBoard.font2, self.datepos, Pos2, graphics.Color(0, 0, 255),
                                      str(Time().get_date()))
        self.offscreen_canvas = ledBoard.matrix.SwapOnVSync(ledBoard.offscreen_canvas)



    def SlideClock(self, pos1, pos2, dir):
        for i in range(5):
            self.print_Clock(pos1, pos2)
            self.offscreen_canvas = ledBoard.matrix.SwapOnVSync(self.offscreen_canvas)
            time.sleep(.25)
            self.offscreen_canvas.Clear()
            if dir == 'down':
                pos1 += 1
                pos2 += 1
            else:
                pos1 -= 1
                pos2 -= 1
        

class initialize:
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.cols = 64
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'
        self.matrix = RGBMatrix(options=self.options)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.font = graphics.Font()
        self.font2 = graphics.Font(1)
        self.font.LoadFont("./10x20.bdf")
        self.font2.LoadFont("./6x9.bdf")


class display_data:
    def __init__(self, _data, _font):
        clock().SlideClock(18,27, 'down')
        self.canvas = ledBoard.offscreen_canvas
        self.data = _data
        self.font = _font 
        # List Index 
        self.x = 0
        self.y = 1
        # Initial Txt Positions
        self.even_txtpos = 64
        self.odd_txtpos = 64
        #  Init variables
        self.odd_txtlen = 0
        self.odd = False
        # True if Done 
        self.odd_done= False
        self.even_done= False
        self.test_print()
        self.run()

    def test_print(self):
        print( str(self.data[0].get('text')))



    def run(self):
        Connected = False
        while not Connected:
            clock().print_Clock(18,27)
            # Start even
            if self.even_done is False:
                self.even_txtlen = graphics.DrawText(self.canvas, self.font, self.even_txtpos, 7,
                                                    graphics.Color(self.data[self.x].get('Color1'),
                                                           self.data[self.x].get('Color2'),
                                                           self.data[self.x].get('Color3')),
                                                    str(self.data[self.x].get('text')))
                self.even_txtpos -= 1

            # Start odd 
            if self.odd_done is False:
                if self.even_txtpos < 64 - self.even_txtlen - 5 or self.odd is True:
                    self.odd_txtlen = graphics.DrawText(self.canvas, self.font, self.odd_txtpos, 7,
                                                    graphics.Color(self.data[self.y].get('Color1'),
                                                           self.data[self.y].get('Color2'),
                                                           self.data[self.y].get('Color3')),
                                                    str(self.data[self.y].get('text')))
                    self.odd_txtpos -=1

            # Next even
            if self.odd_txtpos < 64 - self.odd_txtlen - 5 and self.even_txtpos < 0- self.even_txtlen:
                self.x += 2
                self.even_txtpos = 64
                odd = True

            # Next odd
            if self.even_txtpos < 64 - self.even_txtlen - 5 and self.odd_txtpos < 0- self.odd_txtlen:
                self.y += 2
                self.odd_txtpos = 64

            # If the last item is displayed don't start a new one 
            if self.x > len(self.data)-1 or self.y > len(self.data)-1:
                if len(self.data) % 2 == 0:
                    self.even_done = True
                else:
                    self.odd_done = True

            #  If the last message is off screen kill the process 
            if self.even_done is True:
                if self.odd_txtpos <= 0 - self.odd_txtlen:
                    Connected = True
            if self.odd_done is True:
                if self.even_txtpos <= 0 - self.even_txtlen:
                    Connected = True

            self.canvas = ledBoard.matrix.SwapOnVSync(self.canvas)
            time.sleep(.04)
            self.canvas.Clear()
           




    

if __name__ == "__main__":
    ledBoard = initialize()
    prevTime = None
    while True:
        # If the time changes show a new time 
        if Time().get_time() != prevTime:
            prevTime = Time().get_time()
            clock().print_Clock(18,27)
            time.sleep(5)
            display_data(data().get_stocks('Weekly'), ledBoard.font)


   
   
    # clock().SlideClock(18,27, 'down')
    # time.sleep(5)




