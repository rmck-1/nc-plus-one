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

def test_get_events_request_returns_list_of_all_events(client):
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5