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
    assert data["events"][0]["starts_at"] == "2025-12-31T23:30:00+00:00"

def test_get_events_ID_returns_single_event_with_that_id(client):
    response = client.get("/events/2")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert len(data["event"]) == 1