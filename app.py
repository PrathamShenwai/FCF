from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    city = request.form['city']

    api_key = "c22346bf747c3447ace32de26ea2ef66"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather = data['weather'][0]['main']
        country = data['sys']['country']
        city_name = data['name']

        return render_template('result.html', city=city_name, temperature=temperature, humidity=humidity, weather=weather, country=country)
    else:
        return render_template('result.html', error_message="City not found.")

if __name__ == '__main__':
    app.run(debug=True)
