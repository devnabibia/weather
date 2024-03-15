from pprint import pprint

from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # check for empty string or string with only spaces
    if not bool(city.strip()):
        city = "Nairobi"

    weather_data = get_current_weather(city)

    # error handling
    if not weather_data['cod'] == 200:
        if not weather_data['cod'] == 404:
            return render_template('error.html', error='city not found')
        elif not weather_data['cod'] == 401:
            return render_template('error.html', error='unauthorized')
        elif not weather_data['cod'] == 429:
            return render_template('error.html', error='too many requests')
        else:
            return render_template('error.html', error='unknown error')
    return render_template(
        "weather.html",
        title=weather_data['name'],
        status=weather_data['weather'][0]['description'].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
