import requests
import json
import datetime
from fpdf import FPDF
import tkinter as tk
from PIL import ImageTk, Image
import pyttsx3
from tkinter import messagebox


class WeatherAppGUI:
    def __init__(self, root):
        # Initialize the Weather App GUI
        self.api_key = "e00407ec6dd9fcb91abc6ad6b99e9a76"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("500x700")

        # Create date label
        dt = datetime.datetime.now()
        self.date_label = tk.Label(root, text="Date: " + dt.strftime('%d %B'), bg='white', font=("bold", 15))
        self.date_label.place(x=5, y=130)

        # Create time label
        self.hour_label = tk.Label(root, text="Time: " + dt.strftime('%I : %M %p'), bg='white', font=("bold", 15))
        self.hour_label.place(x=5, y=160)

        # Create city search entry
        self.city_name = tk.StringVar()
        self.city_entry = tk.Entry(root, textvariable=self.city_name, width=45)
        self.city_entry.grid(row=1, column=0, ipady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        # Create search button
        self.search_button = tk.Button(root, text="Search", command=self.get_forecast)
        self.search_button.grid(row=1, column=1, padx=5, sticky=tk.W+tk.E+tk.N+tk.S)

        # Create weather details labels
        self.city_label = tk.Label(root, text="City: ", width=0, bg='white', font=("bold", 15))
        self.city_label.place(x=10, y=63)
        self.country_label = tk.Label(root, text="Country: ", width=0, bg='white', font=("bold", 15))
        self.country_label.place(x=185, y=63)
        self.temp_label = tk.Label(root, text="...", width=0, bg='white', font=("Helvetica", 110), fg='black')
        self.temp_label.place(x=10, y=220)
        self.humidity_label = tk.Label(root, text="Humidity (in percent): ", width=0, bg='white', font=("bold", 15))
        self.humidity_label.place(x=3, y=400)
        self.weather_label = tk.Label(root, text="Weather: ", width=0, bg='white', font=("bold", 15))
        self.weather_label.place(x=3, y=430)
        self.note_label = tk.Label(root, text="All temperatures in degree Celsius", bg='white', font=("italic", 10))
        self.note_label.place(x=95, y=495)

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Set default background image
        default_image_path = 'default.jpg'
        self.set_background_image(default_image_path)

    def read_aloud(self):

        # Convert text to speech and provide voice feedback
        self.engine.setProperty('rate', 150)  # Adjust the voice speed (words per minute)
        self.engine.setProperty('volume', 1)  # Set the volume (0.0 to 1.0)

        self.engine.say("City you have chosen is: " + self.city_entry.get())
        self.engine.say("Temperature is: " + str(self.current_temperature) + " degrees Celsius")
        self.engine.say("Humidity is: " + str(self.humidity) + " percent")
        self.engine.say("Weather is: " + self.weather)
        self.engine.say("Country is: " + self.country)

        self.engine.runAndWait()

    def get_forecast(self):

        # Get the forecast for the entered city

        try:
            city = self.city_entry.get()
            complete_url = self.base_url + "appid=" + self.api_key + "&q=" + city + "&units=metric"
        
            response = requests.get(complete_url)
            data = response.json()
        
            if data["cod"] != "404":
                # Extract the weather data from the API response
                y = data['main']
                self.current_temperature = y['temp']
                self.humidity = y['humidity']
        
                self.current_pressure = y["pressure"]
        
                z = data['sys']
                self.country = z['country']
                city_name = data['name']
        
                self.weather = data['weather'][0]['main']
        
                # Change background image based on weather condition
                image_path = self.get_image_path(self.weather)
                self.set_background_image(image_path)

        
                # Update the weather details labels with the retrieved data
                self.temp_label.configure(text=self.current_temperature)
                self.humidity_label.configure(text="Humidity (in percent): " + str(self.humidity))
                self.city_label.configure(text="City: " + city_name)
                self.country_label.configure(text="Country: " + self.country)
                self.weather_label.configure(text="Weather: " + self.weather)

                # Add a button for report generation
                self.report_button = tk.Button(root, text="Generate Report", command=self.convert_to_pdf)
                self.report_button.grid(row=2, column=1, padx=5, sticky=tk.W+tk.E+tk.N+tk.S)

                # Add a button for next 5 days forecast report generation
                self.forecast_button = tk.Button(root, text="Future Forecast Report", command=self.future_forecast)
                self.forecast_button.grid(row=4, column=1, padx=5, sticky=tk.W+tk.E+tk.N+tk.S)

                # Add a button for next 5 days forecast report generation
                self.audio_button = tk.Button(root, text="Audio", command=self.read_aloud)
                self.audio_button.grid(row=6, column=1, padx=5, sticky=tk.W+tk.E+tk.N+tk.S)

        
            else:
                # Clear the weather details labels if city is not found
                self.temp_label.configure(text="...")
                self.humidity_label.configure(text="Humidity (in percent): ")
                self.city_label.configure(text="City Not Found")
                self.country_label.configure(text="")
                self.weather_label.configure(text="Weather: ")
        
        except:

            messagebox.showerror('Input Error','Please enter the city name correctly')

    def convert_to_pdf(self):

        self.pdf.cell(100,10,"City: " +
                            self.city_entry.get().upper(),ln=2 , align='L')

        self.pdf.cell(100,10,"Temperature (in kelvin unit) = " +
                            str(self.current_temperature),ln=2 , align='L')
        
        self.pdf.cell(100,10,"Atmospheric pressure (in hPa unit) = " +
                            str(self.current_pressure),ln=2 , align='L')
        
        self.pdf.cell(100,10,"Humidity (in percentage) = " +
                            str(self.humidity),ln=2 , align='L')
        
        self.pdf.cell(100,10,"Description = " +
                            str(self.weather),ln=2 , align='L')
        
        self.pdf.output('weather.pdf','F')

    
    def get_image_path(self, weather):
        # Map weather condition to image filename
        weather_images = {
            'clear': 'clearsky.jpg',
            'clouds': 'clouds.jpeg',
            'rain': 'rain.jpg',
            'thunderstorm': 'thunderstorm.jpeg',
            'snow': 'snow.jpg',
        }

        # Get the image filename based on the weather condition
        image_filename = weather_images.get(weather.lower(), 'default.jpg')

        # Return the image file path
        return image_filename

    def set_background_image(self, image_path):
        # Load the background image using PIL
        image = Image.open(image_path)

        # Resize the image to fit the window size
        image = image.resize((500, 700), Image.ANTIALIAS)

        # Convert the PIL image to Tkinter-compatible image
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the label as the background of the root window
        background_label.image = self.background_image

        # Set the stacking order of the label
        background_label.lower()


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
            "q": self.city_entry.get(),
            "appid": self.api_key,
            "units": "metric"  # Change to "imperial" for Fahrenheit
        }

        self.forecast_pdf.cell(100,10,"City: " +
                            self.city_entry.get().upper(),ln=2 , align='L')
        
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract relevant information from the response
            forecasts = data['list']

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

                    self.add_cell_future(date.split(' ')[0],temperature,weather_desc,humidity,wind_speed)
                    current_date = date.split(' ')[0]
                else:
                    pass

            self.forecast_pdf.output('future_weather.pdf','F')

        else:
            print("Error occurred while fetching weather data.")


    def convert_to_pdf(self):

        country = self.country_label.cget("text").split(": ")[1]

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()

        # Add content to the PDF
        pdf.set_font('Arial','BU',30)
        pdf.cell(180,10,"WEATHER CONDITION REPORT",ln=2,align='C')
        pdf.set_font('Arial','B',16)
        pdf.cell(100, 10, "City: " + self.city_entry.get().upper(), ln=2, align='L')
        pdf.cell(100, 10, "Temperature: " + str(self.current_temperature) + "°C", ln=2, align='L')
        pdf.cell(100, 10, "Humidity: " + str(self.humidity), ln=2, align='L')
        pdf.cell(100, 10, "Weather: " + self.weather, ln=2, align='L')
        pdf.cell(100, 10, "Country: " + country, ln=2, align='L')

        # Save the PDF file
        pdf.output('weather_report.pdf','F')



if __name__ == '__main__':
    # Create the root window
    root = tk.Tk()
    # Create an instance of the WeatherAppGUI
    app = WeatherAppGUI(root)
    # Start the Tkinter event loop
    root.mainloop()
