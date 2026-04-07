import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_homepage_contains_title(client):
    response = client.get('/')
    assert b'Weather Dashboard' in response.data