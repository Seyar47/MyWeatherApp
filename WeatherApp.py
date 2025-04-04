import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton,
                            QButtonGroup)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.temp_unit = 'F'  # Default temperature unit
        self.current_temp_k = None  # Store Kelvin temperature
        self.setup_ui_elements()
        self.initUI()    

    def setup_ui_elements(self):
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        
        # Temperature unit selection
        self.temp_unit_group = QButtonGroup(self)
        self.fahrenheit_radio = QRadioButton("°F", self)
        self.celsius_radio = QRadioButton("°C", self)
        self.fahrenheit_radio.setChecked(True)
        self.temp_unit_group.addButton(self.fahrenheit_radio)
        self.temp_unit_group.addButton(self.celsius_radio)
        
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setMinimumSize(400, 600)
        
        # Create layouts and stuff
        main_layout = QVBoxLayout()
        unit_layout = QHBoxLayout()
        
        # Add the componenets and widgets to unit layout
        unit_layout.addWidget(self.fahrenheit_radio)
        unit_layout.addWidget(self.celsius_radio)
        
        # Add all widgets to main layout
        main_layout.addWidget(self.city_label)
        main_layout.addWidget(self.city_input)
        main_layout.addLayout(unit_layout)
        main_layout.addWidget(self.get_weather_button)
        main_layout.addWidget(self.temperature_label)
        main_layout.addWidget(self.emoji_label)
        main_layout.addWidget(self.description_label)
        
        # this is some spacing 
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        self.setLayout(main_layout)

        # center align all stuff
        for label in [self.city_label, self.temperature_label, 
                     self.emoji_label, self.description_label]:
            label.setAlignment(Qt.AlignCenter)

        self.setObjectNames()
        self.apply_styles()
        
        self.get_weather_button.clicked.connect(self.get_weather)
        self.fahrenheit_radio.toggled.connect(self.update_temperature_display)
        self.celsius_radio.toggled.connect(self.update_temperature_display)

    def setObjectNames(self):
        widgets = {
            self.city_label: "city_label",
            self.city_input: "city_input",
            self.get_weather_button: "get_weather_button",
            self.temperature_label: "temperature_label",
            self.emoji_label: "emoji_label",
            self.description_label: "description_label",
            self.fahrenheit_radio: "temp_unit_radio",
            self.celsius_radio: "temp_unit_radio"
        }
        for widget, name in widgets.items():
            widget.setObjectName(name)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
            }
            QLabel, QPushButton {
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#city_label {
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLineEdit#city_input {
                font-size: 28px;
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: white;
            }
            QPushButton#get_weather_button {
                font-size: 24px;
                font-weight: bold;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #2980b9;
            }
            QLabel#temperature_label {
                font-size: 64px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: 'Segoe UI Emoji';
            }
            QLabel#description_label {
                font-size: 36px;
                color: #34495e;
            }
            QRadioButton#temp_unit_radio {
                font-size: 20px;
                color: #2c3e50;
                spacing: 8px;
            }
            QRadioButton#temp_unit_radio::indicator {
                width: 20px;
                height: 20px;
            }
        """)

    def get_weather(self):
        api_key = "204b0c26b35429da87d30c44af50a3f9"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            if data["cod"] == 200:
                self.current_temp_k = data["main"]["temp"]  # the kelvin temperture is store here
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            self.handle_http_error(response.status_code)
        except requests.exceptions.RequestException as e:
            self.display_error(f"Connection Error:\n{str(e)}")

    def handle_http_error(self, status_code):
        error_messages = {
            400: "Bad request:\nPlease check your input",
            401: "Unauthorized:\nInvalid API key",
            403: "Forbidden:\nAccess is denied",
            404: "Not found:\nCity not found",
            500: "Internal Server Error:\nPlease try again later",
            502: "Bad gateway:\nInvalid response from server",
            503: "Service Unavailable:\nServer is down",
            504: "Gateway Timeout:\nNo response from server"
        }
        message = error_messages.get(status_code, f"HTTP error occurred: {status_code}")
        self.display_error(message)

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px; color: #e74c3c;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def update_temperature_display(self):
        if self.current_temp_k is not None:
            self.display_weather({"main": {"temp": self.current_temp_k}, 
                                "weather": [{"id": self.last_weather_id, 
                                           "description": self.last_description}]})

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 64px; color: #2c3e50;")
        self.last_weather_id = data["weather"][0]["id"]
        self.last_description = data["weather"][0]["description"]
        
        # based on which unit is selected convert temperature
        if self.fahrenheit_radio.isChecked():
            temp = (self.current_temp_k * 9/5) - 459.67
            unit = "°F"
        else:
            temp = self.current_temp_k - 273.15
            unit = "°C"

        self.temperature_label.setText(f"{temp:.1f}{unit}")
        self.emoji_label.setText(self.get_weather_emoji(self.last_weather_id))
        self.description_label.setText(self.last_description.capitalize())

    @staticmethod
    def get_weather_emoji(weather_id):
        weather_emojis = {
            range(200, 233): "⛈️",  
            range(300, 322): "🌧️",  
            range(500, 532): "🌧️",  
            range(600, 623): "❄️",  
            range(701, 742): "🌫️",  
            range(762, 763): "🌋",  
            range(771, 772): "💨",  
            range(781, 782): "🌪️",  
            range(800, 801): "☀️", 
            range(801, 805): "☁️",  
        }
        
        return next((emoji for id_range, emoji in weather_emojis.items() 
                    if weather_id in id_range), "")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())