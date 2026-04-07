import pytest
from unittest.mock import patch, MagicMock
from app.services import get_weather, get_coordinates

def test_get_weather_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "current": {
            "temperature_2m": 20.0,
            "wind_speed_10m": 10.0,
            "weather_code": 0
        }
    }
    mock_response.raise_for_status = MagicMock()

    with patch("app.services.requests.get", return_value=mock_response):
        result = get_weather()

    assert result["success"] == True
    assert result["temperature"] == 20.0
    assert result["wind_speed"] == 10.0

def test_get_weather_failure():
    with patch("app.services.requests.get", side_effect=Exception("API error")):
        result = get_weather()

    assert result["success"] == False
    assert result["temperature"] is None

def test_get_coordinates_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{
            "name": "Buenos Aires",
            "country": "Argentina",
            "latitude": -34.61,
            "longitude": -58.37
        }]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("app.services.requests.get", return_value=mock_response):
        result = get_coordinates("Buenos Aires")

    assert result is not None
    assert result["name"] == "Buenos Aires"
    assert result["latitude"] == -34.61

def test_get_coordinates_not_found():
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status = MagicMock()

    with patch("app.services.requests.get", return_value=mock_response):
        result = get_coordinates("ciudadinexistente123")

    assert result is None

def test_get_coordinates_failure():
    with patch("app.services.requests.get", side_effect=Exception("error")):
        result = get_coordinates("Buenos Aires")

    assert result is None