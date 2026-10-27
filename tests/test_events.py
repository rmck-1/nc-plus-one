import os
os.environ["ENV"] = "test"

from fastapi.testclient import TestClient
from main import app

import pytest
from db.seed.seed import drop_and_seed_tables

@pytest.fixture(autouse=True)
def seed_test_db():
    drop_and_seed_tables()

@pytest.fixture()
def client():
    return TestClient(app)

def test_get_events_request_returns_dictionary_with_all_events_in_list_as_value(client):
    response = client.get("/events")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert len(data["events"]) == 5

def test_get_events_returns_dictionary_list_ordered_by_start_date_ascending(client):
    response = client.get("/events")
    data = response.json()
    assert data["events"][0]["starts_at"] == "2025-12-31T23:30:00Z"

def test_get_events_venue_id_parameter_returns_dictionary_with_all_events_that_have_that_id(client):
    response = client.get("/events?venue_id=3")
    data = response.json()
    assert len(data["events"]) == 2

def test_get_events_organiser_id_parameter_returns_dictionary_with_all_events_that_have_that_id(client):
    response = client.get("/events?organiser_id=1")
    data = response.json()
    assert len(data["events"]) == 1

def test_get_events_returns_venue_details_joined_from_venues_table(client):
    response = client.get("/events")
    data = response.json()
    assert data["events"][0]["venue_name"] == "venue_b"
    assert data["events"][0]["venue_address"] == "address_b"
    assert data["events"][0]["venue_capacity"] == 50

def test_get_events_ID_returns_single_event_with_that_id(client):
    response = client.get("/events/2")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert len(data["event"]) == 1
    assert data["event"][0]["title"] == "event_a"

def test_get_event_id_returns_venue_details_joined_from_venues_table(client):
    response = client.get("/events/2")
    data = response.json()
    assert data["event"][0]["venue"] == "venue_a"

def test_get_events_id_returns_404_when_id_does_not_exist(client):
    response = client.get("/events/99")
    data = response.json()
    assert response.status_code == 404
    assert data["error"]["message"] == "Event not found"

def test_get_events_id_returns_400_when_invalid_str_input_provided(client):
    invalid_input = "one"
    response = client.get(f"/events/{invalid_input}")
    data = response.json()
    assert response.status_code == 400
    assert data["error"][0]["message"] == f"Invalid input: '{invalid_input}'"

