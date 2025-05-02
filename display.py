from waveshare_epd import epd7in5_V2_color  # デバイスによって違う
import time
from PIL import Image

# 初期化
epd = epd7in5_V2_color.EPD()
epd.init()
epd.Clear()

# 画像の読み込み（事前に作成したもの）
image = Image.open("weather_7color_preview.png")

# 表示
epd.display(epd.getbuffer(image))
time.sleep(5)
