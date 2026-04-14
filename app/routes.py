from flask import Blueprint, render_template, request
from app.services import get_weather, get_coordinates, get_forecast

main = Blueprint('main', __name__)

@main.route('/')
def index():
    city = request.args.get('city', '').strip()
    compare = request.args.get('compare', '').strip()
    location = None
    weather = None
    forecast = None
    compare_location = None
    compare_weather = None

    if city:
        location = get_coordinates(city)
        if location:
            weather = get_weather(location['latitude'], location['longitude'])
            forecast = get_forecast(location['latitude'], location['longitude'])
        else:
            weather = {"success": False, "not_found": True}
    else:
        location = {"name": "Mendoza", "country": "Argentina"}
        weather = get_weather()
        forecast = get_forecast()

    if compare:
        compare_location = get_coordinates(compare)
        if compare_location:
            compare_weather = get_weather(compare_location['latitude'], compare_location['longitude'])
        else:
            compare_weather = {"success": False, "not_found": True}

    return render_template(
        'index.html',
        weather=weather,
        city=city,
        location=location,
        forecast=forecast,
        compare=compare,
        compare_location=compare_location,
        compare_weather=compare_weather
    )

@main.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': '2024-01-01T00:00:00Z'}, 200