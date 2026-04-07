from flask import Blueprint, render_template
from app.services import get_weather

main = Blueprint('main', __name__)

@main.route('/')
def index():
    weather = get_weather()
    return render_template('index.html', weather=weather)