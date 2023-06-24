import requests, json
import pyttsx3
from fpdf import FPDF

class forecast:

    def __init__(self):
        
        self.api_key = "e00407ec6dd9fcb91abc6ad6b99e9a76"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.city = input("Enter city name: ")
        self.pdf=FPDF()
        self.pdf.add_page()
        self.pdf.set_font('Courier','BU',30)
        self.pdf.cell(180,10,"WEATHER CONDITION REPORT",ln=2,align='C')
        self.pdf.set_font('Courier','B',16)
        self.complete_url = self.base_url + "appid=" + self.api_key + "&q=" + self.city
        self.tts = pyttsx3.init()
        self.get_forecast()
        self.convert_to_pdf()
        self.future_forecast()


    def add_cell_future(self,date,temperature,weather_desc,humidity,wind_speed):
         
        self.forecast_pdf.cell(100,10,"Date: " +
                            date,ln=2 , align='L')

        self.forecast_pdf.cell(100,10,"Temperature (in kelvin unit) = " +
                            str(temperature),ln=2 , align='L')
        
        self.forecast_pdf.cell(100,10,"Wind Speed = " +
                            str(wind_speed),ln=2 , align='L')
        
        self.forecast_pdf.cell(100,10,"Humidity (in percentage) = " +
                            str(humidity),ln=2 , align='L')
        
        self.forecast_pdf.cell(100,10,"Description = " +
                            str(weather_desc),ln=2 , align='L')  

        self.forecast_pdf.cell(100,10,"---------------------------------------------------------",ln=2 , align='L') 

    
    def future_forecast(self):

        self.forecast_pdf = FPDF()
        self.forecast_pdf.add_page()
        self.forecast_pdf.set_font('Courier','BU',30)
        self.forecast_pdf.cell(180,10,"NEXT 5 DAYS WEATHER REPORT",ln=2,align='C')
        self.forecast_pdf.set_font('Courier','B',16)
        
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "metric"  # Change to "imperial" for Fahrenheit
        }

        self.forecast_pdf.cell(100,10,"City: " +
                            self.city.upper(),ln=2 , align='L')
        
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract relevant information from the response
            forecasts = data['list']

            # Print the weather forecast for the next 5 days
            print(f"Weather forecast for {self.city} (next 5 days):")

            date = forecasts[0]['dt_txt']
            current_date = date.split(' ')[0]
            temperature = forecasts[0]['main']['temp']
            weather_desc = forecasts[0]['weather'][0]['description']
            humidity = forecasts[0]['main']['humidity']
            wind_speed = forecasts[0]['wind']['speed']

            self.add_cell_future(current_date,temperature,weather_desc,humidity,wind_speed)

            for forecast in forecasts:
                date = forecast['dt_txt']
                if current_date != date.split(' ')[0]:
                    temperature = forecast['main']['temp']
                    weather_desc = forecast['weather'][0]['description']
                    humidity = forecast['main']['humidity']
                    wind_speed = forecast['wind']['speed']

                    print("Date:", date.split(' ')[0])
                    print(f"Temperature: {temperature}°C")
                    print(f"Weather: {weather_desc}")
                    print(f"Humidity: {humidity}%")
                    print(f"Wind Speed: {wind_speed} m/s")
                    print("--------------------------------------")
                    self.add_cell_future(date.split(' ')[0],temperature,weather_desc,humidity,wind_speed)
                    current_date = date.split(' ')[0]
                else:
                    pass

            self.forecast_pdf.output('future_weather.pdf','F')

        else:
            print("Error occurred while fetching weather data.")

    def convert_to_pdf(self):

        self.pdf.cell(100,10,"City: " +
                            self.city.upper(),ln=2 , align='L')

        self.pdf.cell(100,10,"Temperature (in kelvin unit) = " +
                            str(self.current_temperature),ln=2 , align='L')
        
        self.pdf.cell(100,10,"Atmospheric pressure (in hPa unit) = " +
                            str(self.current_pressure),ln=2 , align='L')
        
        self.pdf.cell(100,10,"Humidity (in percentage) = " +
                            str(self.current_humidity),ln=2 , align='L')
        
        self.pdf.cell(100,10,"Description = " +
                            str(self.weather_description),ln=2 , align='L')
        
        self.pdf.output('weather.pdf','F')

    def get_forecast(self):

        self.response = requests.get(self.complete_url)

        self.data = self.response.json()

        if self.data["cod"] != "404":
 
            self.output = self.data["main"]
        
            self.current_temperature = self.output["temp"]
        
            self.current_pressure = self.output["pressure"]
        
            self.current_humidity = self.output["humidity"]
        
            z = self.data["weather"]
        
            self.weather_description = z[0]["description"]
        
            # print(" Temperature (in kelvin unit) = " +
            #                 str(self.current_temperature) +
            #     "\n atmospheric pressure (in hPa unit) = " +
            #                 str(self.current_pressure) +
            #     "\n humidity (in percentage) = " +
            #                 str(self.current_humidity) +
            #     "\n description = " +
            #                 str(self.weather_description))  

            speak =  "Temperature "+str(self.current_temperature) + "Kelvin" + "atmospheric pressure " + str(self.current_pressure) + "Hpa" + "Humidity " +str(self.current_humidity)+"percent" + str(self.weather_description)
            self.tts.say(speak)
            self.tts.runAndWait()
        
        else:
            print(" City Not Found ")

if __name__ == '__main__':
    forecast()

        
         
                     
