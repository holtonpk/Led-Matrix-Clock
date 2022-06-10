from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics

def clear():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    matrix = RGBMatrix(options=options)
    offscreen_canvas = matrix.CreateFrameCanvas()
    offscreen_canvas.Clear()

if __name__ == '__main__':
    clear()
