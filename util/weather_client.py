import requests
from datetime import datetime

class WeatherClient:
    def __init__(self, city="Tokyo", env_path=".env"):
        self.city = city
        self.api_key = self.load_api_key(env_path)

    def load_api_key(self, filepath):
        try:
            with open(filepath, "r") as f:
                for line in f:
                    if line.strip().startswith("API_KEY="):
                        return line.strip().split("=", 1)[1]
        except FileNotFoundError:
            print(f"{filepath} が見つかりませんでした。")
        return None

    def get_weekly_weather(self):
        if not self.api_key:
            print("APIキーが読み込めませんでした。")
            return [], []

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={self.api_key}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            timestamps = []
            temperatures = []
            for entry in data['list']:
                timestamp = entry['dt']
                temp = entry['main']['temp']
                dt = datetime.utcfromtimestamp(timestamp)
                timestamps.append(dt.strftime("%m-%d %H:%M"))
                temperatures.append(temp)
            return timestamps, temperatures
        else:
            print("天気情報の取得に失敗しました。")
            return [], []


weekly_weather = WeatherClient()
timestamps, temperatures = weekly_weather.get_weekly_weather()


print("Timestamps:")
print(timestamps)
print("\nTemperatures:")
print(temperatures)