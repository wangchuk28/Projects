import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.city_label=QLabel("Enter City:",self)
        self.city_input=QLineEdit(self)
        self.weather_button=QPushButton("Get Weather",self)
        self.description_label=QLabel(self)
        self.temperature_label=QLabel(self)
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Weather App")
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.weather_button)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.temperature_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.description_label.setObjectName("description_label")
        self.city_input.setObjectName("city_input")
        self.weather_button.setObjectName("weather_button")
        self.temperature_label.setObjectName("temperature_label")

 #CSS       
 
            
        self.setStyleSheet("""                                          
             QPushButton#weather_button{
                    font-family: Arial;
                    font-size: 20px;
                    padding: 10px;
                    }
             QLabel#city_label{
                    font-weight: bold;
                    font-size: 30px;
                    font-family: Times New Roman;
                    }

            QLabel#description_label{
                    font-weight: bold;
                    font-size: 55px;
                    font-family: Times New Roman;
                    }
            QLineEdit#city_input{
                    background-color: black;
                    border: 1px solid #ccc;
                    border-radius: 12px;
                    padding: 5px;
                    font-size: 45px;
                    color: white;
                    }
            QLabel#temperature_label{
                    font-weight: bold;
                    font-size: 55px;
                    font-family: Times New Roman;
                    font-style: italic;
                    }
             """)

        self.weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key="318c4a0c4339e3b9f984d064ff8d0d1a"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        


        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            print(data)
            if data["cod"]==200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request. Please check the city name.")
                case 404:
                    self.display_error("City not found.")
                case 401:
                    self.display_error("Unauthorized. Please check your API key.")
                case 403:
                    self.display_error("Forbidden. You might not have access to this resource.")
                case 500:
                    self.display_error("Internal Server Error. Please try again later.")
                case 502:
                    self.display_error("Bad gateway. Please try again later.")
                case 503:
                    self.display_error("Service unavailable. Please try again later.")
                case 504:
                    self.display_error("Gateway timeout. Please try again later.")
                case _:
                    self.display_error(f"HTTP error occurred:\n {http_error}")

        except requests.exceptions.ConnectionError :
            self.display_error("Connection error occurred. Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out. Please try again later.")
        except requests.redirects.TooManyRedirects:
            self.display_error("Too many redirects. Please check the URL.")
        except requests.exceptions.RequestException as request_error:
            self.display_error(f"An error occurred:\n {request_error}")

    def display_error(self, message):
        self.description_label.setStyleSheet("font-size: 30px;")
        self.description_label.setText(message)
        self.temperature_label.clear()
        

    def display_weather(self, data):
        temperature=data["main"]["temp"]
        temperature_celsius=temperature-273.15
        print(temperature_celsius)
        self.temperature_label.setText(f"{temperature_celsius:.0f}°C")
        self.description_label.setStyleSheet("font-size: 40px;")

        weather_description=data["weather"][0]["description"]
        self.description_label.setText(weather_description.capitalize())
        print(weather_description)



if __name__=="__main__":
    app=QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
