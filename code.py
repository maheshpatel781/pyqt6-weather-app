import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
)

from PyQt6.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App with Toggle °C/°F")
        self.unit = "C"  # Default temperature unit
        self.setup_ui()

    def setup_ui(self):
        self.city_label = QLabel("Enter city name:")
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather")
        self.toggle_button = QPushButton("°C/°F")
        self.temp_label = QLabel("")
        self.emoji_label = QLabel("")
        self.desc_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.get_weather_button)
        btn_layout.addWidget(self.toggle_button)
        layout.addLayout(btn_layout)

        layout.addWidget(self.temp_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.desc_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.toggle_button.clicked.connect(self.toggle_unit)

    def get_weather(self):
        city = self.city_input.text()
        api_key = "007dc7e02afd03face8fa0328daabe04"  # Replace with your actual OpenWeatherMap API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            temp_k = data['main']['temp']
            self.temp_c = temp_k - 273.15
            self.temp_f = (temp_k * 9/5) - 459.67
            description = data['weather'][0]['description']
            weather_id = data['weather'][0]['id']
            emoji = self.get_weather_emoji(weather_id)

            self.display_temperature()
            self.emoji_label.setText(emoji)
            self.desc_label.setText(description.capitalize())
        except requests.exceptions.HTTPError:
            self.display_error("HTTP Error occurred")
        except requests.exceptions.ConnectionError:
            self.display_error("Check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out")
        except requests.exceptions.RequestException:
            self.display_error("Network error occurred")

    def display_error(self, message):
        self.temp_label.setText(message)
        self.emoji_label.setText("")
        self.desc_label.setText("")

    def display_temperature(self):
        if self.unit == "C":
            self.temp_label.setText(f"{self.temp_c:.0f}°C")
        else:
            self.temp_label.setText(f"{self.temp_f:.0f}°F")

    def toggle_unit(self):
        self.unit = "F" if self.unit == "C" else "C"
        self.display_temperature()

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 781:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "🌡️"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
