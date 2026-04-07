import requests

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

def get_coordinates(city: str):
    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "es"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("results"):
            return None
        result = data["results"][0]
        return {
            "name": result["name"],
            "country": result["country"],
            "latitude": result["latitude"],
            "longitude": result["longitude"]
        }
    except Exception:
        return None

def get_weather(latitude=-32.89, longitude=-68.83):
    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ["temperature_2m", "wind_speed_10m", "weather_code"],
                "timezone": "auto"
            },
            timeout=10
        )
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
    

    