
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Football Match Center" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_matches_api(client):
    response = client.get("/api/matches")
    assert response.status_code == 200

    matches = response.get_json()
    assert len(matches) == 4
    assert matches[0]["home"] == "Manchester City"


def test_match_data_has_required_fields(client):
    response = client.get("/api/matches")
    matches = response.get_json()

    for match in matches:
        assert "home" in match
        assert "away" in match
        assert "status" in match
