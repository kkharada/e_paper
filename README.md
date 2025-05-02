✅ 1. デバイスの基本情報

    解像度：800 × 480

    対応色：7色（黒・白・赤・黄・青・緑・オレンジ）

    通信：SPI

    ドライバ名：epd7in3f

✅ 2. セットアップ手順（Raspberry Pi）
📦 ドライバのインストール

git clone https://github.com/waveshare/e-Paper
cd e-Paper/RaspberryPi_JetsonNano/python/
sudo pip3 install -r requirements.txt

✅ SPIの有効化（未設定の場合）

sudo raspi-config
→ Interface Options → SPI → <Yes>
→ 再起動

✅ 3. 表示用Pythonコード（自作画像を表示）

以下は Pillow で作った画像 weather_7color_preview.png を電子ペーパーに表示する例です。

from waveshare_epd import epd7in3f
from PIL import Image
import time

# 初期化
epd = epd7in3f.EPD()
epd.init()
epd.Clear()

# 画像読み込み（800x480, RGB, 7色以内）
image = Image.open("weather_7color_preview.png")

# 表示
epd.display(epd.getbuffer(image))

# 終了（省電力）
epd.sleep()

✅ 4. 注意点
項目	内容
✅ 解像度	800×480固定。異なると表示されません。
✅ 色数	7色以外は表示されない。RGB値を指定パレットに制限してください。
🕒 表示速度	フル更新は20〜30秒かかります（正常）
✅ 画像形式	PillowのImage.new("RGB", (800, 480))で生成したもの
✅ 5. カスタム画像の作成も簡単！

先に作成したPythonスクリプト（weather_7color_preview.png生成用）と、この表示スクリプトを組み合わせれば、定期的に天気情報を更新して電子ペーパーに反映できます。