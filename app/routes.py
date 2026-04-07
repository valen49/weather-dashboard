from flask import Blueprint, render_template, request
from app.services import get_weather, get_coordinates, get_forecast

main = Blueprint('main', __name__)

@main.route('/')
def index():
    city = request.args.get('city', '').strip()
    location = None
    weather = None
    forecast = None

    if city:
        location = get_coordinates(city)
        if location:
            weather = get_weather(location['latitude'], location['longitude'])
            forecast = get_forecast(location['latitude'], location['longitude'])
        else:
            weather = {"success": False, "not_found": True}
    else:
        weather = get_weather()
        forecast = get_forecast()

    return render_template('index.html', weather=weather, city=city, location=location, forecast=forecast)