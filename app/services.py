import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

DEFAULT_PARAMS = {
    "latitude": -32.89,
    "longitude": -68.83,
    "current": ["temperature_2m", "wind_speed_10m", "weather_code"],
    "timezone": "America/Argentina/Buenos_Aires"
}

def get_weather(latitude=-32.89, longitude=-68.83):
    try:
        params = {
            **DEFAULT_PARAMS,
            "latitude": latitude,
            "longitude": longitude,
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current"]
        return {
            "temperature": current["temperature_2m"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"],
            "success": True
        }
    except Exception:
        return {
            "temperature": None,
            "wind_speed": None,
            "weather_code": None,
            "success": False
        }