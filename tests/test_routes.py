import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_returns_200(client):
    with patch("app.routes.get_weather") as mock_weather, \
         patch("app.routes.get_forecast") as mock_forecast:
        mock_weather.return_value = {"success": False}
        mock_forecast.return_value = {"days": [], "success": False}
        response = client.get('/')
    assert response.status_code == 200

def test_index_with_city(client):
    with patch("app.routes.get_coordinates") as mock_coords, \
         patch("app.routes.get_weather") as mock_weather, \
         patch("app.routes.get_forecast") as mock_forecast:
        mock_coords.return_value = {
            "name": "Mendoza",
            "country": "Argentina",
            "latitude": -32.89,
            "longitude": -68.83
        }
        mock_weather.return_value = {"success": True, "temperature": 20.0, "wind_speed": 10.0, "icon": "☀️"}
        mock_forecast.return_value = {"days": [], "success": True}
        response = client.get('/?city=Mendoza')
    assert response.status_code == 200

def test_index_with_invalid_city(client):
    with patch("app.routes.get_coordinates") as mock_coords:
        mock_coords.return_value = None
        response = client.get('/?city=ciudadinexistente123')
    assert response.status_code == 200

def test_index_with_compare(client):
    with patch("app.routes.get_coordinates") as mock_coords, \
         patch("app.routes.get_weather") as mock_weather, \
         patch("app.routes.get_forecast") as mock_forecast:
        mock_coords.return_value = {
            "name": "Mendoza",
            "country": "Argentina",
            "latitude": -32.89,
            "longitude": -68.83
        }
        mock_weather.return_value = {"success": True, "temperature": 20.0, "wind_speed": 10.0, "icon": "☀️"}
        mock_forecast.return_value = {"days": [], "success": True}
        response = client.get('/?city=Mendoza&compare=BuenosAires')
    assert response.status_code == 200

def test_index_with_invalid_compare(client):
    with patch("app.routes.get_coordinates") as mock_coords, \
         patch("app.routes.get_weather") as mock_weather, \
         patch("app.routes.get_forecast") as mock_forecast:
        mock_coords.side_effect = [
            {
                "name": "Mendoza",
                "country": "Argentina",
                "latitude": -32.89,
                "longitude": -68.83
            },
            None
        ]
        mock_weather.return_value = {"success": True, "temperature": 20.0, "wind_speed": 10.0, "icon": "☀️"}
        mock_forecast.return_value = {"days": [], "success": True}
        response = client.get('/?city=Mendoza&compare=ciudadinexistente123')
    assert response.status_code == 200