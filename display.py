#!/usr/bin/env python3
import logging
import time
from PIL import Image
from pathlib import Path

import sys
sys.path.append('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')

# ディスプレイ設定
EPD_WIDTH = 800
EPD_HEIGHT = 480
PALETTE = {
    'black': 0,
    'white': 1,
    'red': 2,
    'yellow': 3,
    'blue': 4,
    'green': 5,
    'orange': 6
}

class EPaper7Color:
    def __init__(self, image_path):
        self.image_path = image_path
        self.epd = None
        self._init_display()

    def _init_display(self):
        """ディスプレイ初期化 (自動検出機能付き)"""
        try:
            from waveshare_epd import epd7in5_V2
            self.epd = epd7in5_V2.EPD()
            self.epd.init()
            logging.info(f"7色電子ペーパー検出: {self.epd.__class__.__name__}")
            return True
        except ImportError:
            logging.warning("Waveshareライブラリが見つかりません（開発モード）")
        except Exception as e:
            logging.error(f"初期化エラー: {e}")
        return False

    def _convert_image(self):
        """7色パレットに最適化した画像変換"""
        img = Image.open(self.image_path)
        if img.size != (EPD_WIDTH, EPD_HEIGHT):
            img = img.resize((EPD_WIDTH, EPD_HEIGHT))
        
        # 7色化処理 (例: 赤成分を強調)
        img = img.convert("RGB")
        pixels = img.load()
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                if r > 160 and g < 100 and b < 100:  # 赤色検出
                    pixels[x, y] = (255, 0, 0)  # 赤に変換
        return img

    def display(self, retry=3):
        """画像表示 (自動リトライ機能付き)"""
        if not self.epd:
            logging.warning("ディスプレイ未接続のためスキップ")
            return False

        img = self._convert_image()
        
        for attempt in range(retry):
            try:
                self.epd.display(self.epd.getbuffer(img))
                self.epd.sleep()
                logging.info(f"表示成功 (試行 {attempt + 1}/{retry})")
                return True
            except Exception as e:
                logging.error(f"表示失敗: {e}")
                time.sleep(2)
                if attempt == retry - 1:
                    self.epd.sleep()
        return False

if __name__ == "__main__":
    # ログ設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 画像パス (main.pyで生成されたもの)
    IMAGE_PATH = "./weather_dashboard.png"
    
    # 画像存在確認
    if not Path(IMAGE_PATH).exists():
        logging.error(f"画像が見つかりません: {IMAGE_PATH}")
        exit(1)

    # 電子ペーパー制御
    epaper = EPaper7Color(IMAGE_PATH)
    if not epaper.display():
        logging.warning("表示に失敗しました")