import matplotlib.pyplot as plt
import matplotlib as mpl

# ??????????????????????????

# ??1: ???????????????
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'IPAPGothic', 'TakaoPGothic', 'VL PGothic']

# デバイス設定
EPD_WIDTH = 800
EPD_HEIGHT = 480
import numpy as np
from datetime import datetime
from matplotlib import gridspec
from util.weather_client import WeatherClient

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'e-Paper/RaspberryPi_JetsonNano/python/lib'))
# デバイス設定

# デバイス設定
EPD_WIDTH = 800
EPD_HEIGHT = 480

# カラーパレット
COLORS = {
    'background': 'white',
    'text': 'black',
    'accent': 'red',
    'highlight': 'orange',
    'primary': 'blue',
    'secondary': 'green',
    'muted': 'gray'
}

output_path = './weather_dashboard.png'

# フォント設定
#plt.style.use('seaborn')

plt.style.use('seaborn-v0_8')  # ???seaborn????
plt.style.use('ggplot')        # ??????
plt.style.use('default')       # ?????????

try:
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    plt.rcParams['axes.unicode_minus'] = False
except:
    plt.rcParams['font.family'] = 'sans-serif'

def main():
    # データ取得
    client = WeatherClient(city="Tokyo")
    timestamps, temperatures = client.get_weekly_weather()
    current_date = datetime.now().strftime("%Y/%m/%d")
    current_time = datetime.now().strftime("%H:%M")

    # 日次データ処理
    dates = []
    daily_temps = []
    current_day = ""
    temps_for_day = []

    for ts, temp in zip(timestamps, temperatures):
        day = ts.split()[0]
        if day != current_day:
            if current_day:
                dates.append(current_day)
                daily_temps.append(round(np.mean(temps_for_day), 1))
            current_day = day
            temps_for_day = []
        temps_for_day.append(temp)

    if temps_for_day:
        dates.append(current_day)
        daily_temps.append(round(np.mean(temps_for_day), 1))

    # ダッシュボード作成
    fig = plt.figure(figsize=(EPD_WIDTH/100, EPD_HEIGHT/100), 
                    facecolor=COLORS['background'])
    gs = gridspec.GridSpec(3, 1, height_ratios=[1, 0.8, 2])

    # 1. ヘッダー部分
    ax_header = plt.subplot(gs[0], facecolor=COLORS['background'])
    ax_header.text(0.5, 0.7, "東京の天気", 
                 fontsize=28, ha='center', va='center',
                 color=COLORS['text'], fontweight='bold')
    ax_header.text(0.5, 0.3, f"{current_date} {current_time} 更新", 
                 fontsize=16, ha='center', va='center', color=COLORS['text'])
    ax_header.axis('off')

    # 2. 現在の天気
    ax_current = plt.subplot(gs[1], facecolor=COLORS['background'])
    today_temp = daily_temps[0]
    ax_current.text(0.3, 0.7, f"{today_temp}°C", 
                  fontsize=48, ha='center', va='center',
                  color=COLORS['accent'], fontweight='bold')

    # 環境情報
    env_info = [
        ("湿度", f"{65}%", COLORS['primary']),
        ("風速", f"{3}m/s", COLORS['secondary']),
        ("気圧", f"{1012}hPa", COLORS['muted'])
    ]

    for i, (label, value, color) in enumerate(env_info):
        ax_current.text(0.25 + i*0.25, 0.2, f"{label}\n{value}", 
                      fontsize=14, ha='center', va='center', color=color)
    ax_current.axis('off')

    # 3. 週間予報 (線グラフ)
    ax_weekly = plt.subplot(gs[2], facecolor=COLORS['background'])
    line = ax_weekly.plot(daily_temps, 
                        color=COLORS['primary'], 
                        linewidth=3,
                        marker='o',
                        markersize=8,
                        markerfacecolor='white',
                        markeredgecolor=COLORS['primary'],
                        markeredgewidth=2)

    # 今日のポイントを強調
    ax_weekly.plot(0, daily_temps[0], 'o',
                  markersize=12,
                  color=COLORS['accent'])

    # 温度ラベル
    for i, (date, temp) in enumerate(zip(dates, daily_temps)):
        color = COLORS['accent'] if i == 0 else COLORS['text']
        ax_weekly.text(i, temp+0.8, f"{temp}°", 
                     ha='center', va='bottom', 
                     fontsize=12, color=color)

    # 日付ラベル（日本式: 月/日 形式に変更）
    short_dates = [f"{int(d.split('-')[1])}/{int(d.split('-')[0])}" for d in dates]  # 先頭の0を除去
    ax_weekly.set_xticks(range(len(dates)))
    ax_weekly.set_xticklabels(short_dates, rotation=45, fontsize=12)

    # 最高・最低気温
    max_temp = max(daily_temps)
    min_temp = min(daily_temps)
    ax_weekly.axhline(max_temp, color=COLORS['highlight'], linestyle=':', alpha=0.5)
    ax_weekly.axhline(min_temp, color=COLORS['secondary'], linestyle=':', alpha=0.5)
    ax_weekly.text(len(dates)-0.5, max_temp+0.5, f"最高: {max_temp}°C", 
                  ha='right', va='bottom', color=COLORS['highlight'])
    ax_weekly.text(len(dates)-0.5, min_temp-0.5, f"最低: {min_temp}°C", 
                  ha='right', va='top', color=COLORS['secondary'])

    # グラフ装飾
    ax_weekly.grid(axis='y', linestyle='--', alpha=0.3)
    ax_weekly.spines['top'].set_visible(False)
    ax_weekly.spines['right'].set_visible(False)
    ax_weekly.set_ylim(min_temp-2, max_temp+2)

    # レイアウト調整
    plt.tight_layout(pad=3)
    plt.subplots_adjust(hspace=0.4)

    # 画像保存
    
    plt.savefig(output_path, dpi=120, facecolor=COLORS['background'],
               bbox_inches='tight', pad_inches=0.2)
    plt.close()

    print(f"ダッシュボード画像を保存しました: {output_path}")

# 電子ペーパー表示関数
def display_on_epaper(image_path):
    from PIL import Image
    from waveshare_epd import epd7in3f
    
    try:
     epd = epd7in3f.EPD()
     epd.init()
     epd.Clear()

     image = Image.open(image_path)
     epd.display(epd.getbuffer(image))

     epd.sleep()
     print("電子ペーパーに表示しました")
    except Exception as e:
     print(f"表示エラー: {e}")



if __name__ == "__main__":
    main()

    # 実行
    display_on_epaper(output_path)
