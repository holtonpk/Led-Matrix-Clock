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

class run:
    def __init__(self, Test='False', Type=None):
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

        stocktimes=(5,10,20,25,35,40,50,55)
        markethours = (7,8,9,10,11,12,1,2,3)
        cryptotimes=(30,0)
        self.ClockMoved = False
        self.TokenFail = False

        done  = False
        while not done:
            self.clock(True, False)
            if Test == 'True':
                if int(self.minute) %1 == 0:
                    if Type == 'S':
                        try:
                            self.getStocks()
                            self.print(self.textlist, self.font2, 7, True, False)
                        except PermissionError as e:
                            print(e)
                            b.run()
                        done = True
                        break
                    if Type == 'T':
                        self.getTokens()
                        self.print(self.textlist, self.font, 23, False, True)
                        done = True
                        break
            else:
                if int(self.minute) in stocktimes :
                    if int(self.hour) in markethours:
                        try:
                            if self.TokenFail is False:
                                self.getStocks()
                                self.print(self.textlist, self.font2, 7, True, False)
                        except PermissionError as e:
                            # self.TokenFail = True
                            try:
                                b.run()
                            except:
                                pass

                    self.offscreen_canvas.Clear()
                if int(self.minute) in cryptotimes:
                    self.getTokens()
                    self.print(self.textlist, self.font, 23, False, True)
                self.offscreen_canvas.Clear()

    def clock(self, Solo, crypto):
        month = datetime.now().date().month
        day = datetime.now().date().day
        self.date = str(month) + '/' + str(day)
        self.minute = datetime.now().minute
        self.hour = datetime.now().hour
        if int(self.hour) > 12:
            self.hour -= 12
        minute = self.minute
        if int(self.minute) < 10:
            minute = "0"+str(self.minute)
        self.time = str(self.hour) + ":" + str(minute)
        if crypto is False:
            if Solo is True:
                if crypto is False:
                    if self.time != self.prevtime:
                        self.TokenFail = False
                        self.prevtime = self.time
                        try:
                            self.offscreen_canvas.Clear()
                        except:
                            pass
                        if self.ClockMoved is True:
                            self.SlideClock(23, 32, 'down')
                        self.printClock(18,27)
                        self.ClockMoved = False
                        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

            else:
                if self.ClockMoved is False:
                    self.SlideClock(18, 27, 'up')
                self.printClock(23, 32)
                self.ClockMoved = True

    def SlideClock(self,pos1, pos2, dir, ):
        for i in range(5):
            self.printClock(pos1, pos2)
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
            time.sleep(.25)
            self.offscreen_canvas.Clear()
            if dir == 'up':
                pos1 += 1
                pos2 += 1
            else:
                pos1 -= 1
                pos2 -= 1



    def printClock(self, Pos1, Pos2):
        # 23 32
        self.Ttxt = graphics.DrawText(self.offscreen_canvas, self.font, 10, Pos1, graphics.Color(0, 0, 255),
                                      str(self.time))
        self.Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2, 10, Pos2, graphics.Color(0, 0, 255),
                                      str(self.date))
        self.offscreen_canvas.Clear()
        self.timepos = 32 - (self.Ttxt / 2)
        self.datepos = 32 - (self.Dtxt / 2)
        self.Ttxt = graphics.DrawText(self.offscreen_canvas, self.font, self.timepos, Pos1, graphics.Color(0, 0, 255),
                                      str(self.time))
        self.Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2, self.datepos, Pos2, graphics.Color(0, 0, 255),
                                      str(self.date))

    def getTokens(self):
        web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/dfb29047e37a436fbbf8e723722f3b9c'))
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
        self.textlist = []
        for coin in CoinList:
            addr = coin.get("ADDR")
            token = coin.get("TOKEN")
            img = coin.get("IMG")
            contract = web3.eth.contract(address=addr, abi=abi)
            latestData = contract.functions.latestRoundData().call()
            price = round(int(latestData[1]) / 100000000, 2)
            text = str(token) + " $" + f"{price:,}"
            self.textlist.append({'text': text, 'Color1': coin.get("Color"),
                                  'Color2': coin.get("Color1"),'Color3': coin.get("Color2"), 'IMG':img})

    def getStocks(self):
        ListToGet = 'Top'
        c = auth.client_from_token_file(config.token_path, config.api_key, asyncio=False)
        Watchlsit = c.get_watchlists_for_single_account(config.account_id).json()
        Tickerlist = []
        for x in Watchlsit:
            if x.get('name') == ListToGet:
                watchlist = x.get('watchlistItems')
                for stocks in watchlist:
                    Tickerlist.append(stocks.get('instrument').get('symbol'))
        self.textlist = []
        for tickers in Tickerlist:
            open = c.get_quote(tickers).json().get(tickers).get('closePrice')
            current = c.get_quote(tickers).json().get(tickers).get('lastPrice')
            percentchange = str(round((1 - (float(open) / float(current))) * 100, 2))
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
            text = tickers + ' ' + percentchange + '%'+' $ ' + str(current)
            self.textlist.append({'text': text, 'Color1': color1,
                                  'Color2': color2, 'Color3': color3, 'IMG': img})

    def Alertmess(self, TEXT, Font, TextPos, Stock):
        pos = 64
        timeposy =18
        dateposy = 27
        loop2 = False
        loops = 0
        connected = False
        while not connected:
            if Stock is True:
                self.clock(False, False)
            else:
                self.clock(True,True)
                Ttxt = graphics.DrawText(self.offscreen_canvas, self.font,
                                         self.timepos, timeposy, graphics.Color(0, 0, 255),
                                         str(self.time))
                Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2,
                                         self.datepos,dateposy, graphics.Color(0, 0, 255),
                                         str(self.date))
                timeposy -=1
                dateposy +=1
                self.timepos+=1
                self.datepos +=1

            txtlen = graphics.DrawText(self.offscreen_canvas, Font, pos, TextPos,
                                       graphics.Color(randint(0, 255),
                                                      randint(0, 255),
                                                      randint(0, 255)),
                                       TEXT)


            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
            time.sleep(.04)
            self.offscreen_canvas.Clear()
            if pos == 0 - txtlen:
                loop2 = True
            if loop2 is False:
                pos -= 1
            else:
                pos += 1
            if pos == 64:
                loops += 1
                loop2 = False
            if loops == 1:
                connected = True
                break


    def print(self, List, Font, TextPos, ClockON, Crypto):
        if Crypto is True:
           self.Alertmess('CRYPTO ALERT!',Font, TextPos, False)
        else:
            self.Alertmess('STOCK ALERT!',Font, TextPos,True)

        listlen = len(List)
        y = -1
        x = 0
        imlen = 10
        txtlen = 700
        imlen2 = 10
        txtlen2 = 70
        Loop2 = False
        Loop1 = True
        Tpos1 = 64
        Impos1 = 64
        Tpos2 = 64
        ImPos2 = 64
        connected = False
        while not connected:
            if ClockON is True:
                self.clock(False, False)
            if Loop1 is True:
                self.image1 = Image.open(List[x].get('IMG'))
                self.image1.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
                imlen, img_height = self.image1.size
                Loop1 = False
            self.offscreen_canvas.SetImage(self.image1.convert('RGB'), Impos1)
            Impos1 -= 1
            if Impos1 < 64 - imlen - 5:
                txtlen = graphics.DrawText(self.offscreen_canvas, Font, Tpos1, TextPos,
                                           graphics.Color(List[x].get('Color1'),
                                                          List[x].get('Color2'),
                                                          List[x].get('Color3')),
                                           str(List[x].get('text')))
                Tpos1 -= 1
            if Tpos1 == 64 - txtlen - 5 or Loop2 is True:
                if Tpos1 == 64 - txtlen - 5:
                    y += 2
                    if y == listlen:
                        self.lastLoop(x, Tpos1, List, Font, TextPos, Crypto, ClockON)
                        connected = True
                        break
                    Tpos2 = 64
                    ImPos2 = 64
                    self.image2 = Image.open(List[y].get('IMG'))
                    self.image2.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
                    imlen2, img_height2 = self.image2.size
                self.offscreen_canvas.SetImage(self.image2.convert('RGB'), ImPos2)
                ImPos2 -= 1
                Loop2 = True
            if ImPos2 < 64 - imlen2 - 5:
                txtlen2 = graphics.DrawText(self.offscreen_canvas, Font, Tpos2, TextPos,
                                            graphics.Color(List[y].get('Color1'),
                                                           List[y].get('Color2'),
                                                           List[y].get('Color3')),
                                            str(List[y].get('text')))
                Tpos2 -= 1

            if Tpos2 == 64 - txtlen2 - 5:
                x += 2
                if x == listlen:
                    self.lastLoop(y, Tpos2, List, Font, TextPos, Crypto, ClockON)
                    connected = True
                    break
                Tpos1 = 64
                Impos1 = 64
                Loop1 = True
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

            time.sleep(.04)
            self.offscreen_canvas.Clear()

    def lastLoop(self, var, Tpos, List, Font, TextPos, Crypto, ClockON):
        tpos = 64
        dpos = 64
        timepos =0
        datepos = 0
        done = False
        while not done:
            if ClockON is True:
                self.clock(False, False)
            txtlen = graphics.DrawText(self.offscreen_canvas, Font, Tpos, TextPos,
                                       graphics.Color(List[var].get('Color1'),
                                                      List[var].get('Color2'),
                                                      List[var].get('Color3')),
                                       str(List[var].get('text')))
            Tpos -= 1
            if Crypto is True:
                if Tpos <= 64 - txtlen:
                    self.clock(True, True)
                    Ttxt = graphics.DrawText(self.offscreen_canvas, self.font,
                                             tpos, 18, graphics.Color(0, 0, 255),
                                             str(self.time))
                    Dtxt = graphics.DrawText(self.offscreen_canvas, self.font2,
                                             dpos, 27, graphics.Color(0, 0, 255),
                                             str(self.date))
                    if tpos > timepos:
                        tpos -= 1
                    if dpos > datepos:
                        dpos -=1
                    timepos = 32 - (Ttxt / 2)
                    datepos = 32 - (Dtxt / 2)

            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
            time.sleep(.04)
            self.offscreen_canvas.Clear()
            if Tpos < 0 - txtlen:
                done = True



if __name__ == '__main__':
    try:
        r = run(sys.argv[1], sys.argv[2])
    except:
        r = run()




